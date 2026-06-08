# HandTrackingModule-Python
Control your Windows system volume using hand gestures with OpenCV, MediaPipe, and Pycaw. Adjust volume in real-time by changing the distance between your thumb and index finger.

# Gesture Volume Controller 🎛️✋

Control your Windows system volume using only your hand gestures and a webcam.

This project uses **OpenCV**, **MediaPipe**, and **Pycaw** to track your hand in real-time and adjust the system volume based on the distance between your **thumb** and **index finger**.

## Features

* 🎥 Real-time hand tracking
* 🔊 System volume control using gestures
* ⚡ Adjustable sensitivity multiplier
* 📊 On-screen volume percentage display
* 🖥️ Works with any standard webcam
* 🤖 Powered by MediaPipe hand landmarks

## How It Works

1. The webcam captures video frames.
2. MediaPipe detects and tracks hand landmarks.
3. The distance between the thumb tip and index finger tip is calculated.
4. The distance is mapped to the Windows volume range.
5. The system volume updates instantly.

**Close fingers → Lower volume**

**Move fingers apart → Higher volume**

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Pycaw
* Tkinter

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/gesture-volume-controller.git
cd gesture-volume-controller
```

Install dependencies:

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

## Usage

Run the application:

```bash
python main.py
```

A dialog box will appear asking for a sensitivity multiplier:

* Lower values = more sensitive volume changes
* Higher values = smoother volume changes

After selecting a value:

* Show your hand to the webcam
* Move your thumb and index finger closer or farther apart
* Watch the volume change in real time

Press **ESC** to exit.

## Controls

| Gesture                             | Action           |
| ----------------------------------- | ---------------- |
| Thumb + Index Finger Close Together | Lower Volume     |
| Thumb + Index Finger Far Apart      | Increase Volume  |
| ESC Key                             | Exit Application |

## Requirements

* Windows 10/11
* Python 3.9+
* Webcam

## Future Improvements

* Multiple gesture support
* Mute gesture
* Brightness control
* Custom gesture mapping
* Cross-platform audio support

## Demo

Add a GIF or video here to showcase the project in action.

## License

This project is open source and available under the MIT License.
