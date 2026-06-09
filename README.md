Lazy Scroller

A computer vision-based system that enables hands-free mouse control using hand gestures via a webcam.

Overview

Lazy Scroller uses MediaPipe for real-time hand tracking and translates finger gestures into mouse actions such as cursor movement, clicking, and scrolling.

Features

- Cursor movement using index finger
- Left click using pinch gesture
- Double click using rapid pinch
- Vertical scrolling using two-finger gesture
- Configurable sensitivity and gesture thresholds

Tech Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

Installation

Clone the repository:

git clone https://github.com/HiyaPatwal/Lazy-Scroller.git
cd Lazy-Scroller

Install dependencies:

pip install -r requirements.txt

Usage

Run the application:

python main.py

Ensure your webcam is enabled.

Controls

Index finger up        -> Move cursor  
Pinch (thumb + index) -> Left click  
Rapid pinch           -> Double click  
Index + middle up     -> Scroll  

How It Works

- MediaPipe detects hand landmarks in real time
- Landmark positions determine finger states
- Gestures are mapped to mouse actions using PyAutoGUI
- Cursor movement is smoothed for stability

Configuration

Adjust parameters in main.py:

- PINCH_DISTANCE_THRESHOLD
- SCROLL_MULTIPLIER
- SMOOTHENING
- Bounding box dimensions

Limitations

- Performance depends on lighting conditions
- Requires a stable webcam feed
- Single-hand tracking only
