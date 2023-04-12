import os
import pandas as pd
import cv2
import mediapipe as mp
from .helpers import *

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles

@measure_elapsed_time
def extract_frames(input_dir: str, output_dir: str):
    return input_dir, output_dir

@measure_elapsed_time
def extract_landmarks(input_video: str, output_csv: str) -> None:
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        data = []
        cap = cv2.VideoCapture(input_video)
        # Create output video writer
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Process each frame in input video
        frame_count = 0
        while cap.isOpened():
            # Read next frame from input video
            ret, image = cap.read()
            if not ret:
                break

            results = pose.process(image)

            if not results.pose_landmarks:
                # print("No pose detected in frame {}".format(frame_count))
                data.append({'frame': frame_count, 'landmarks': None})

            if results.pose_landmarks:
                positions = ['nose', 'left_eye_inner', 'left_eye', 'left_eye_outer',
                            'right_eye_inner', 'right_eye', 'right_eye_outer',
                            'left_ear', 'right_ear','mouth_left', 'mouth_right',
                            'left_shoulder', 'right_shoulder','left_elbow', 'right_elbow',
                            'left_wrist', 'right_wrist','left_pinky', 'right_pinky',
                            'left_index', 'right_index','left_thumb', 'right_thumb',
                            'left_hip', 'right_hip','left_knee', 'right_knee',
                            'left_ankle', 'right_ankle','left_heel', 'right_heel',
                            'left_foot_index', 'right_foot_index']

                pose_data = {'frame': frame_count}
                for i, position in enumerate(positions):
                    landmark = results.pose_landmarks.landmark[i]
                    pose_data[f'{position}_x'] = landmark.x
                    pose_data[f'{position}_y'] = landmark.y
                    pose_data[f'{position}_z'] = landmark.z
                data.append(pose_data)

            # Increment frame count
            frame_count += 1

        # Save pose landmarks to CSV file
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)

        cap.release()