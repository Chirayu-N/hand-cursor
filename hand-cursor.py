import cv2
import mediapipe as mp
import pyautogui
import math

# Parameters
showVideo = False
CLICK_THRESHOLD = 0.05

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Calculate screen dimensions
screen_width, screen_height = pyautogui.size()

# Capture and downsample video stream
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640/2)    # 640/2 screen_width/4.725
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480/2)   # 480/2 screen_height/4.725

# Calculate distance between two landmarks
def calculate_distance(landmark1, landmark2):
    return math.hypot(landmark1.x - landmark2.x, landmark1.y - landmark2.y)

# Convert normalized landmark coordinates to screen coordinates
def convert_coordinates(landmark, screen_width, screen_height):
    return int(landmark.x * screen_width), int(landmark.y * screen_height)

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for natural interaction
    img = cv2.flip(img, 1)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if showVideo:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            # Calculate distance between thumb tip and index tip
            distance = calculate_distance(thumb_tip, index_tip)
            
            # Calculate mouse coordinates
            mouse_x, mouse_y = convert_coordinates(index_mcp, screen_width, screen_height)
            
            # Move mouse cursor
            pyautogui.moveTo(mouse_x, mouse_y)
            
            # Click gesture if fingers are sufficiently close
            if distance < CLICK_THRESHOLD:
                pyautogui.click()

    # Optionally display the video feed
    if showVideo:
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
