# # squats/views.py
# from django.shortcuts import render
# from django.http import StreamingHttpResponse
# import cv2
# import mediapipe as mp
# import numpy as np
# import pygame
# import os

# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# audio_dir = '/home/amaanshahk/Desktop/qwerty/squats/static/audio'

# up_audio_file = os.path.join(audio_dir, 'up.mp3')
# down_audio_file = os.path.join(audio_dir, 'down.mp3')

# pygame.mixer.init()

# # Load audio files as pygame.mixer.Sound
# up_sound = pygame.mixer.Sound(up_audio_file)
# down_sound = pygame.mixer.Sound(down_audio_file)

# # Flags to track whether the audio cues have been played
# up_audio_played = False
# down_audio_played = False
# done_audio_played = False

# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return angle

# def play_audio(sound, played_flag):
#     if not played_flag:
#         sound.play()
#         played_flag = True
#     return played_flag

# def count_rep(counter, stage, angle, up_threshold, down_threshold):
#     global up_audio_played, down_audio_played

#     if angle > up_threshold:
#         stage = "up"
#         down_audio_played = play_audio(down_sound, down_audio_played)
#     if angle < down_threshold and stage == 'up':
#         stage = "down"
#         counter += 1
#         print("Rep Count:", counter)
#         up_audio_played = play_audio(up_sound, up_audio_played)

#     # Reset flags when the user is in the "down" stage
#     if stage == 'down':
#         down_audio_played = False
#         up_audio_played = False

#     return counter, stage




# def generate_frames():
#     cap = cv2.VideoCapture(2)
#     squat_counter = 0
#     squat_stage = None
#     squat_up_threshold = 170
#     squat_down_threshold = 80

#     with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.1) as pose:
#         while cap.isOpened():
#             ret, frame = cap.read()

#             if not ret:
#                 break

#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             try:
#                 landmarks = results.pose_landmarks.landmark

#                 # Squat tracking for knee
#                 shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
#                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                 hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
#                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
#                 knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
#                           landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
#                 heel_l = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
#                            landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]

#                 angle_lk = int(calculate_angle(hip_l, knee_l, heel_l))

#                 shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
#                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
#                 hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
#                          landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
#                 knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
#                           landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
#                 heel_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
#                            landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

#                 angle_rk = int(calculate_angle(hip_r, knee_r, heel_r))

#                 avg_knee_angle = (angle_lk + angle_rk) / 2

#                 # Squat tracking for hip
#                 angle_lh = int(calculate_angle(shoulder_l, hip_l, knee_l))
#                 angle_rh = int(calculate_angle(shoulder_r, hip_r, knee_r))
#                 avg_hip_angle = (angle_lh + angle_rh) / 2

#                 # Squat counting based on knee and hip angles
#                 squat_counter, squat_stage = count_rep(squat_counter, squat_stage, avg_knee_angle,
#                                                        squat_up_threshold, squat_down_threshold)

#                 cv2.putText(image, str(angle_lk),
#                             tuple(np.multiply(knee_l, [640, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#                 cv2.putText(image, str(angle_rk),
#                             tuple(np.multiply(knee_r, [640, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#                 # Visualize angles at hip points
#                 cv2.putText(image, str(angle_lh),
#                             tuple(np.multiply(hip_l, [640, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#                 cv2.putText(image, str(angle_rh),
#                             tuple(np.multiply(hip_r, [640, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
#                 # Render detections
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                                            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
#                                            )

#             except Exception as e:
#                 print("Error:", e)

#             cv2.putText(image, 'Squat Reps: ' + str(squat_counter), (10, 25),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
#             ret, jpeg = cv2.imencode('.jpg', image)
#             frame = jpeg.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         cap.release()

# def index(request):
#     return render(request, 'squats/index.html')

# def video_feed(request):
#     return StreamingHttpResponse(generate_frames(),
#                                  content_type='multipart/x-mixed-replace; boundary=frame')


# squats/views.py
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

audio_dir = '/home/amaanshahk/Desktop/qwerty/squats/static/audio'

up_audio_file = os.path.join(audio_dir, 'come-up-higher.mp3')
down_audio_file = os.path.join(audio_dir, 'go_deeper.mp3')

pygame.mixer.init()

# Load audio files as pygame.mixer.Sound
up_sound = pygame.mixer.Sound(up_audio_file)
down_sound = pygame.mixer.Sound(down_audio_file)

# Flags to track whether the audio cues have been played
up_audio_played = False
down_audio_played = False
done_audio_played = False

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

def count_rep(counter, stage, angle, up_threshold, down_threshold):
    global up_audio_played, down_audio_played

    if angle > up_threshold:
        stage = "up"
        down_audio_played = play_audio(down_sound, down_audio_played)
    if angle < down_threshold and stage == 'up':
        stage = "down"
        counter += 1
        print("Rep Count:", counter)
        up_audio_played = play_audio(up_sound, up_audio_played)

    # Reset flags when the user is in the "down" stage
    if stage == 'down':
        down_audio_played = False
        up_audio_played = False

    return counter, stage

def generate_frames():
    cap = cv2.VideoCapture(0)
    squat_counter = 0
    squat_stage = None
    squat_up_threshold = 170
    squat_down_threshold = 80

    # Time and rep count variables
    start_time = time.time()  # Initialize start_time here
    total_reps = 10  # Set your desired total reps
    time_limit = 300  # Set your desired time limit in seconds

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

            # Initialize start time if not done already
            if start_time is None:
                start_time = time.time()

            try:
                landmarks = results.pose_landmarks.landmark

                # Squat tracking for knee
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                heel_l = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]

                angle_lk = int(calculate_angle(hip_l, knee_l, heel_l))

                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                heel_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]

                angle_rk = int(calculate_angle(hip_r, knee_r, heel_r))

                avg_knee_angle = (angle_lk + angle_rk) / 2

                # Squat tracking for hip
                angle_lh = int(calculate_angle(shoulder_l, hip_l, knee_l))
                angle_rh = int(calculate_angle(shoulder_r, hip_r, knee_r))
                avg_hip_angle = (angle_lh + angle_rh) / 2


                squat_counter, squat_stage = count_rep(squat_counter, squat_stage, avg_knee_angle,
                                                       squat_up_threshold, squat_down_threshold)

                cv2.putText(image, str(angle_lk),
                            tuple(np.multiply(knee_l, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)


                cv2.putText(image, str(angle_rk),
                            tuple(np.multiply(knee_r, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Visualize angles at hip points
                cv2.putText(image, str(angle_lh),
                            tuple(np.multiply(hip_l, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(angle_rh),
                            tuple(np.multiply(hip_r, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                           mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                           )
                if avg_knee_angle > squat_up_threshold:
                    feedback_message = "Go Deeper"
                    feedback_color = (0, 0, 255)  # Red color for "Go Deeper"
                    # feedback_sound = down_sound
                elif avg_knee_angle < squat_down_threshold:
                    feedback_message = "Come Up Higher"
                    feedback_color = (255, 0, 0)  # Blue color for "Come Up Higher"
                    # feedback_sound = up_sound
                else:
                    feedback_message = "Good Depth"
                    feedback_color = (0, 255, 0)  # Green color for "Good Depth"
                    # feedback_sound = None  # No sound for "Good Depth"

                # Display feedback message
                cv2.putText(image, feedback_message, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, feedback_color, 2, cv2.LINE_AA)

                # Calculate text size to center arrows below the message
                text_size = cv2.getTextSize(feedback_message, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_width, text_height = text_size

                # Add visual indicators (arrows) based on feedback below the message
                arrow_start_x = 10 + (text_width // 2)
                arrow_start_y = 80 + text_height  # Place below the feedback message

                if avg_knee_angle > squat_up_threshold:
                    cv2.arrowedLine(image, (arrow_start_x, arrow_start_y), (arrow_start_x, arrow_start_y + 25),
                                    (0, 0, 255), 4)  # Red arrow pointing down
                elif avg_knee_angle < squat_down_threshold:
                    cv2.arrowedLine(image, (arrow_start_x, arrow_start_y), (arrow_start_x, arrow_start_y - 25),
                                    (255, 0, 0), 4)  # Blue arrow pointing up
                # # Play audio feedback
                # if feedback_sound:
                #     feedback_sound.play()

            except Exception as e:
                print("Error:", e)

            cv2.putText(image, 'Squat Reps: ' + str(squat_counter), (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Check if the time limit is reached
            if time_limit and time.time() - start_time > time_limit:
                print("Time limit reached. Total Reps:", squat_counter)
                break

            # Check if the target number of reps is reached
            if total_reps and squat_counter >= total_reps:
                print("Target reps reached. Total Reps:", squat_counter)
                break

            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def index(request):
    return render(request, 'squats/index.html')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
