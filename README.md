# AirCursor

A computer vision-based hand tracking system that allows you to control your mouse cursor using hand gestures in the air. No physical mouse needed!

## Features

- **Gesture-Based Cursor Control**: Move your cursor by simply pointing with your index finger
- **Left Click**: Pinch your index finger and thumb together
- **Right Click**: Bring index, thumb, and middle fingers together
- **Scroll**: Use index finger only (other fingers down) and move up/down to scroll
- **Real-time Hand Tracking**: Powered by MediaPipe for accurate hand landmark detection
- **Smooth Cursor Movement**: Built-in smoothing algorithm for stable cursor control
- **Visual Feedback**: Live camera feed with gesture recognition display

## Demo

The system detects your hand through your webcam and translates hand gestures into mouse actions:
- Point to move the cursor
- Pinch to click
- Hold specific gestures to scroll

## Requirements

- Python 3.7+
- Webcam
- Operating System: Windows, macOS, or Linux

### Dependencies

```
opencv-python
mediapipe
pyautogui
numpy
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/adnanpkg/AirCursor.git
cd AirCursor
```

2. Install required packages:
```bash
pip install opencv-python mediapipe pyautogui numpy
```

Or create a `requirements.txt` file with the following content:
```
opencv-python>=4.5.0
mediapipe>=0.10.0
pyautogui>=0.9.53
numpy>=1.21.0
```

Then install:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python "Hand tracking.py"
```

### Gesture Controls

| Gesture | Action | Description |
|---------|--------|-------------|
| **Point with index finger** | Move Cursor | Move your index finger to control cursor position |
| **Index + Thumb pinch** | Left Click | Bring your index finger and thumb tips together |
| **Index + Thumb + Middle pinch** | Right Click | Bring index, thumb, and middle finger tips together |
| **Index finger only (others down)** | Scroll Mode | Keep other fingers down, move index finger up/down to scroll |
| **All fingers up** | Air Cursor Mode | All fingers extended for general cursor movement |

### Controls

- **'q' key**: Quit the application
- The application window shows:
  - Live camera feed with hand tracking overlay
  - Current cursor coordinates
  - Active gesture detection
  - Visual feedback for clicks and gestures

## Configuration

You can adjust the following parameters in the `AirCursorTracker` class:

- `min_detection_confidence`: Hand detection sensitivity (default: 0.8)
- `min_tracking_confidence`: Hand tracking sensitivity (default: 0.7)
- `smoothing`: Cursor smoothing factor (default: 0.3, range: 0-1)
- `click_threshold`: Distance threshold for click detection (default: 30)
- `click_cooldown`: Time between clicks in seconds (default: 0.3)
- `gesture_cooldown`: Time between gesture changes (default: 1.0)

## How It Works

1. **Hand Detection**: Uses MediaPipe's hand tracking solution to detect hand landmarks in real-time
2. **Landmark Extraction**: Identifies key finger positions (thumb, index, middle, ring, pinky tips)
3. **Gesture Recognition**: Calculates distances between fingertips to recognize gestures
4. **Cursor Mapping**: Maps hand position from camera space to screen coordinates
5. **Smoothing**: Applies exponential smoothing for stable cursor movement
6. **Action Execution**: Uses PyAutoGUI to perform mouse actions based on detected gestures

## Troubleshooting

### Common Issues

**Camera not detected:**
- Ensure your webcam is connected and not being used by another application
- Check camera permissions in your OS settings

**Cursor movement is jittery:**
- Increase the `smoothing` parameter (up to 0.7)
- Ensure good lighting conditions
- Keep your hand steady within the camera frame

**Gestures not detected:**
- Adjust `min_detection_confidence` and `min_tracking_confidence`
- Ensure your entire hand is visible in the camera frame
- Check for adequate lighting

**PyAutoGUI failsafe triggered:**
- Move your physical mouse to a corner to trigger failsafe
- This is a safety feature to prevent cursor getting stuck

## Technical Details

- **Framework**: OpenCV for video capture, MediaPipe for hand tracking
- **Hand Landmarks**: Detects 21 landmarks per hand
- **Coordinate System**: Normalized coordinates (0-1) mapped to screen resolution
- **Performance**: Real-time processing at camera frame rate (typically 30 FPS)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available for educational and personal use.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking solution
- [OpenCV](https://opencv.org/) for computer vision functionality
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for GUI automation

## Author

Created by [Adnan](https://github.com/adnanmov)

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/adnanmov/AirCursor).

---

**Note**: This project is for educational purposes. Ensure you have proper lighting and a clear background for best results.
