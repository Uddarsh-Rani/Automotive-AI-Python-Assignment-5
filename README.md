# Driver Monitoring System (DMS)

## Overview

Driver Monitoring System (DMS) is a real-time safety application developed using Python and Computer Vision techniques to monitor driver behavior continuously. The system detects signs of driver fatigue, distraction, head pose deviation, eye closure, yawning, and mobile phone usage while driving.

The objective of this project is to improve road safety by alerting the driver whenever unsafe behavior is detected.

---

## Features

* Eye blink detection
* Drowsiness detection
* Yawning detection
* Head pose estimation
* Mobile phone usage detection
* Real-time alert generation
* Live video monitoring through webcam/mobile camera

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame
* CVZone

---

## Working Principle

The system captures live video input through a camera and processes each frame using facial landmark detection.

### Eye Detection

Facial landmarks around the eyes are tracked continuously. If the eye remains closed beyond a threshold duration, drowsiness is detected.

### Yawning Detection

Mouth landmarks are monitored to calculate mouth opening ratio. Large opening for a certain time indicates yawning.

### Head Pose Detection

Face orientation is tracked to detect if the driver is looking left, right, down, or away from the road.

### Mobile Phone Detection

The system checks whether a mobile phone is visible near the driver's face region and triggers distraction warning.

### Alert Mechanism

Whenever unsafe conditions are identified, an audio alert is generated immediately.

---

## Project Structure

driver-monitoring-system/
│── main.py
│── alarm.wav
│── README.md

---

## Installation

Install required libraries:

pip install opencv-python mediapipe numpy pygame cvzone

---

## Run the Project

python main.py

---

## Output

The system opens live camera feed and displays:

* Eye status
* Head direction
* Drowsiness alert
* Mobile alert

---

## Applications

* Automotive driver safety systems
* Smart vehicle cabin monitoring
* ADAS development
* Driver fatigue prevention systems

---

## Future Improvements

* Infrared camera support
* Better night-time detection
* Deep learning-based distraction classification
* Integration with vehicle CAN systems

---

## Author

Developed as an academic automotive safety project.
