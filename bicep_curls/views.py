# bicep_curls/views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp
import numpy as np
import pygame
import os
import time  # Add this import

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Set the path to the directory containing audio files
audio_dir = '/home/amaanshahk/Desktop/qwerty/bicep_curls/static/audio'

# Define audio file paths for left arm
left_down = os.path.join(audio_dir, 'down.mp3')
right_down = os.path.join(audio_dir, 'down.mp3')

pygame.mixer.init()

# Load audio files as pygame.mixer.Sound
left_down_sound = pygame.mixer.Sound(left_down)
right_down_sound = pygame.mixer.Sound(right_down)

# Flags to track whether the audio cues have been played for left arm
left_down_audio_played = False
right_down_audio_played = False

# Counter variables for left and right arms
left_counter = 0
right_counter = 0
left_stage = None
right_stage = None

# Time and rep count variables
start_time = None
total_reps = 100
time_limit = 300

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def play_audio(sound, played_flag):
    if not played_flag:
        sound.play()
        played_flag = True
    return played_flag

def bicep_curls_logic(landmarks, stage, angle, counter, audio_sound, audio_played):
    global start_time, left_counter, right_counter

    # Initialize start time
    if start_time is None:
        start_time = time.time()

    # Bicep curl counter logic
    if angle > 165:
        stage = "down"
    if angle < 20 and stage == 'down':
        stage = "up"
        counter += 1
        print("Rep Count:", counter)

    # Play audio cues based on the stage
    if stage == "up":
        audio_played = play_audio(audio_sound, audio_played)

    # Reset flags when the user is in the "down" stage
    if stage == 'down':
        audio_played = False

    # Check if the time limit is reached
    if time_limit and time.time() - start_time > time_limit:
        print("Time limit reached. Total Reps:", counter)
        return 'done', counter, False  # Add 'done' stage to indicate completion

    # Check if the target number of reps is reached
    if total_reps and counter >= total_reps:
        print("Target reps reached. Total Reps:", counter)
        return 'done', counter, False  # Add 'done' stage to indicate completion

    return stage, counter, audio_played

def generate_frames():
    global left_counter, right_counter, left_stage, right_stage, left_down_audio_played, right_down_audio_played, start_time

    cap = cv2.VideoCapture(0)

    # Bicep curl counters
    left_counter = 0
    right_counter = 0
    left_stage = None
    right_stage = None
    left_down_audio_played = False
    right_down_audio_played = False
    start_time = None

    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.2) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Extract landmarks for left arm
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Calculate angle for left arm
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                # Extract landmarks for right arm
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angle for right arm
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize angles without labels
                cv2.putText(image, f"{int(left_angle)}",
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, f"{int(right_angle)}",
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Bicep curl logic for left arm
                left_stage, left_counter, left_down_audio_played = bicep_curls_logic(
                    landmarks, left_stage, left_angle, left_counter, left_down_sound, left_down_audio_played
                )

                # Bicep curl logic for right arm
                right_stage, right_counter, right_down_audio_played = bicep_curls_logic(
                    landmarks, right_stage, right_angle, right_counter, right_down_sound, right_down_audio_played
                )

            except Exception as e:
                print("Error:", e)

            cv2.putText(image, 'Left Arm Reps: ' + str(left_counter), (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, 'Right Arm Reps: ' + str(right_counter), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Exit the loop if both arms complete the session
            if left_stage == 'done' and right_stage == 'done':
                break

    cap.release()
    
def index(request):
    return render(request, 'bicep_curls/index.html')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')