# pushups/views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp
import numpy as np
import pygame
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

audio_dir = '/home/amaanshahk/Desktop/qwerty/pushups/static/audio'
up_audio_file = os.path.join(audio_dir, 'up.mp3')
down_audio_file = os.path.join(audio_dir, 'down.mp3')

pygame.mixer.init()

# Load audio files as pygame.mixer.Sound
up_sound = pygame.mixer.Sound(up_audio_file)
down_sound = pygame.mixer.Sound(down_audio_file)

# Flags to track whether the audio cues have been played
up_audio_played = False
down_audio_played = False

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

def count_pushup(counter, avg_knee_angle, avg_elbow_angle, knees_straight):
    global up_audio_played, down_audio_played

    # Check if the knees are straight
    if knees_straight:
        # Check if the elbow angle is going from up to down
        if avg_elbow_angle > 165 and not up_audio_played:
            up_audio_played = play_audio(down_sound, down_audio_played)
        elif avg_elbow_angle < 70 and up_audio_played:
            counter += 1
            up_audio_played = play_audio(up_sound, up_audio_played)

    return counter

def generate_frames():
    cap = cv2.VideoCapture(0)
    pushup_counter = 0

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.1) as pose:
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
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]

                # Extract landmarks for right arm
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

                # Calculate angles for left arm
                left_knee_angle = calculate_angle(left_hip, left_knee, left_heel)
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                # Calculate angles for right arm
                right_knee_angle = calculate_angle(right_hip, right_knee, right_heel)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Calculate average angles for both arms
                avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
                avg_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2

                # Check if the knees are straight (use an appropriate threshold)
                knees_straight = (avg_knee_angle > 165)

                # Display angles on the body
                cv2.putText(image, str(int(left_knee_angle)),
                            tuple(np.multiply(left_knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(int(left_elbow_angle)),
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(int(right_knee_angle)),
                            tuple(np.multiply(right_knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(int(right_elbow_angle)),
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Count push-ups based on average knee and elbow angles and knee straight condition
                pushup_counter = count_pushup(pushup_counter, avg_knee_angle, avg_elbow_angle, knees_straight)

            except Exception as e:
                print("Error:", e)

            cv2.putText(image, 'Push-ups: ' + str(pushup_counter), (10, 30),
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

    cap.release()

def index(request):
    return render(request, 'pushups/index.html')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
