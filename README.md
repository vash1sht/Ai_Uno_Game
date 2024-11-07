# UNO Card Detection Game
Version: 1.0.0

Welcome to the UNO Card Detection Game, an interactive game developed in Python using Pygame and YOLO object detection. This game allows users to detect UNO cards through a camera feed or by uploading an image, making for an engaging way to interact with UNO cards digitally.

Developed by BOT_MATRIX.

# Project Overview
<img width="901" alt="Screenshot 2024-11-07 at 01 22 22" src="https://github.com/user-attachments/assets/20a1b644-23f4-45e5-9d91-5ae0255d0253">

The UNO Card Detection Game is a Pygame-based application that uses a pre-trained YOLO model to identify UNO cards in real-time. Users can initiate the game with a main menu and choose between real-time card detection via the camera or by uploading an image of UNO cards. The game visually labels detected cards and displays them on the screen, adding an immersive experience.

## Features:
- Real-Time Card Detection: Use a camera to detect UNO cards in real-time.
- Image Upload Detection: Upload images of UNO cards for detection.
- Main Menu and Transitions: Smooth fade-in and fade-out transitions between screens.
- Sound Effects: Interactive sound effects for button clicks and screen transitions.
- UNO Card Labeling: Visual labeling of card types and colors.

## Installation:
### Prerequisites
- Python 3.x
- Required libraries: opencv-python, pygame, tk, ultralytics

### Steps
1. Clone the repository:
```
git clone https://github.com/vash1sht/Ai_Uno_Game.git
cd Ai_Uno_Game
```
2. Install dependencies:
```
pip install opencv-python pygame ultralytics
```

## Usage
1. Start the application:
```
python main.py
```
2. Use the main menu to:
- Start real-time card detection using the camera.
- Upload an image for card detection.
- Exit the game.

3. In the game screen, click on:
- Camera: Initiates real-time UNO card detection.
- Image: Allows image upload for UNO card detection.
- Back: Returns to the main menu.
- Exit: Quit the game by selecting "Quit" from the main menu.
