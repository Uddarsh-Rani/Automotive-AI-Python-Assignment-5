import cv2
import mediapipe as mp
from math import hypot
import pygame
import time
import csv

# ---------------------------------
# AUDIO INITIALIZATION
# ---------------------------------
pygame.mixer.init()

mild_sound = pygame.mixer.Sound("D:\Educational_space\SIT_Pune\SEM_2\AutomotiveAI\DriverMonitoringSystem\mild_alert.wav")
heavy_sound = pygame.mixer.Sound("D:\Educational_space\SIT_Pune\SEM_2\AutomotiveAI\DriverMonitoringSystem\heavy_alert.wav")
phone_sound = pygame.mixer.Sound("D:\Educational_space\SIT_Pune\SEM_2\AutomotiveAI\DriverMonitoringSystem\phone_alert.wav")

def stop_all_audio():
    mild_sound.stop()
    heavy_sound.stop()
    phone_sound.stop()

# ---------------------------------
# MEDIAPIPE SETUP
# ---------------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# ---------------------------------
# LANDMARKS
# ---------------------------------
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14]

# ---------------------------------
# EAR FUNCTION
# ---------------------------------
def eye_aspect_ratio(eye_points, landmarks, w, h):
    points = []

    for p in eye_points:
        lm = landmarks[p]
        x = int(lm.x * w)
        y = int(lm.y * h)
        points.append((x, y))

    v1 = hypot(points[1][0]-points[5][0], points[1][1]-points[5][1])
    v2 = hypot(points[2][0]-points[4][0], points[2][1]-points[4][1])
    h_dist = hypot(points[0][0]-points[3][0], points[0][1]-points[3][1])

    return (v1+v2)/(2*h_dist)

# ---------------------------------
# MOUTH FUNCTION
# ---------------------------------
def mouth_ratio(landmarks, w, h):
    p1 = landmarks[MOUTH[0]]
    p2 = landmarks[MOUTH[1]]

    y1 = int(p1.y*h)
    y2 = int(p2.y*h)

    return abs(y1-y2)

# ---------------------------------
# EVENT LOGGING
# ---------------------------------
def log_event(event):
    with open("event_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%H:%M:%S"), event])

# ---------------------------------
# CAMERA SETUP
# ---------------------------------
cap = cv2.VideoCapture(0)

# For mobile IP webcam use:
# cap = cv2.VideoCapture("http://YOUR_IP:4747/video")

# ---------------------------------
# FIX FRAME SIZE FOR MOBILE CAMERA
# ---------------------------------
frame_width = 640
frame_height = 480

# MJPG codec works better for mobile streams
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

out = cv2.VideoWriter(
    "final_dms_output.avi",
    fourcc,
    20.0,
    (frame_width, frame_height)
)

# Verify writer
if not out.isOpened():
    print("VideoWriter failed to open")

# ---------------------------------
# VARIABLES
# ---------------------------------
closed_frames = 0
down_frames = 0
up_frames = 0

mild_triggered = False
heavy_triggered = False
phone_triggered = False

scroll_x = 640

# ---------------------------------
# MAIN LOOP
# ---------------------------------
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame,(640,480))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    h,w,_ = frame.shape

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:

            landmarks = face_landmarks.landmark

            # EAR
            left_ear = eye_aspect_ratio(LEFT_EYE, landmarks, w, h)
            right_ear = eye_aspect_ratio(RIGHT_EYE, landmarks, w, h)

            avg_ear = (left_ear + right_ear)/2

            # HEAD POSITION
            nose = landmarks[1]
            nose_x = int(nose.x*w)
            nose_y = int(nose.y*h)

            if nose_x < 250:
                head_status = "LOOKING LEFT"

            elif nose_x > 390:
                head_status = "LOOKING RIGHT"

            elif nose_y > 270:
                head_status = "LOOKING DOWN"
                down_frames += 1
                up_frames = 0

            else:
                head_status = "CENTER"
                up_frames += 1

                if up_frames > 10:
                    down_frames = 0

            # PHONE DISTRACTION
            if down_frames > 25:
                cv2.putText(frame,"PHONE DISTRACTION!",(50,200),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

                if not phone_triggered:
                    stop_all_audio()
                    phone_sound.play(-1)
                    log_event("Phone Distraction")
                    phone_triggered = True
            else:
                phone_sound.stop()
                phone_triggered = False

            # YAWNING
            mouth_open = mouth_ratio(landmarks,w,h)

            if mouth_open > 20:
                cv2.putText(frame,"YAWNING",(50,250),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),3)

            # DROWSINESS
            if avg_ear < 0.22:
                closed_frames += 1
            else:
                closed_frames = 0
                stop_all_audio()
                mild_triggered = False
                heavy_triggered = False

            # Mild
            if 15 < closed_frames <= 30:
                cv2.putText(frame,"MILD DROWSINESS",(50,100),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)

                if not mild_triggered:
                    stop_all_audio()
                    mild_sound.play(-1)
                    log_event("Mild Drowsiness")
                    mild_triggered = True

            # Heavy
            elif closed_frames > 30:
                cv2.putText(frame,"HEAVY DROWSINESS",(50,100),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

                if not heavy_triggered:
                    stop_all_audio()
                    heavy_sound.play(-1)
                    log_event("Heavy Drowsiness")
                    heavy_triggered = True

            else:
                cv2.putText(frame,"ALERT",(50,100),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

            # DISPLAY
            cv2.putText(frame,f"EAR:{avg_ear:.2f}",(50,150),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

            cv2.putText(frame,head_status,(50,300),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    # SCROLLING RIBBON
    ribbon = "Rani Uddarsh, MTech AT, 25070152008"

    cv2.rectangle(frame,(0,450),(640,480),(50,50,50),-1)

    cv2.putText(frame,ribbon,(scroll_x,470),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    scroll_x -= 2

    if scroll_x < -400:
        scroll_x = 640

    # SAVE VIDEO
    out.write(frame)

    cv2.imshow("Advanced DMS", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------------------------
# RELEASE
# ---------------------------------
cap.release()
out.release()
cv2.destroyAllWindows()