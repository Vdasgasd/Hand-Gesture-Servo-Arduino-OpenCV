import cv2
import mediapipe as mp
import serial
import numpy as np


arduino = serial.Serial('COM3', 9600)

def send_servo_signal(angle):
    arduino.write(bytes(str(angle), 'utf-8'))

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the image and detect hands
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the landmark coordinates for thumb and index finger
                thumb_x = hand_landmarks.landmark[4].x
                thumb_y = hand_landmarks.landmark[4].y
                index_x = hand_landmarks.landmark[8].x
                index_y = hand_landmarks.landmark[8].y

                # Draw landmarks on the image
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Calculate the angle between thumb and index finger
                angle = int(np.degrees(np.arctan2(thumb_y - index_y, thumb_x - index_x)) + 180)

                # Send servo signal based on the angle
                send_servo_signal(angle)

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

arduino.close()
cap.release()
cv2.destroyAllWindows()
