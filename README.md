# Hand Cursor
A simple but fun way to interact with your laptop using gestures like the Apple Vision Pro and other VR products.

## Features
- Move your hand to move the cursor
- Pinch with your thumb and index finger to left-click
- (WIP) other smart gestures like scrolling, zoom, and more
- (WIP) improved input smoothing to reduce jittering
- (WIP) allow for multiple hands to be tracked at once

## How It Works
We first feed in the video stream from the laptop's webcam using the `cv2` Python library. 

Using the stream, we can use Google's MediaPipe Hand Landmarker (`mediapipe` library) to identify the major landmark positions on a hand on the screen. Set ``showVideo = True`` in the main `hand-cursor.py` file to view the video feed with annotated landmarks. 

![hand-landmarks](hand-landmarks.png)

We then map the positions from the video space to the laptop screen space, moving the cursor to the appropriate spot using ``pyautogui``. There is still some improvement to be made in this part—the movement is a bit jittery, but creating minimum thresholds for movement can reduce responsiveness for the user.