import os
import numpy as np
import pandas as pd
import time

def measure_elapsed_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.3f} seconds")
        return result
    return wrapper

@measure_elapsed_time
def batch_data_augmentation(input_dir: str):
    joint_pairs = [('right_shoulder', 'right_elbow'), ('right_elbow', 'right_wrist'), ('right_hip', 'right_knee'), ('right_knee', 'right_ankle'), ('right_ankle', 'right_foot_index'), ('left_shoulder', 'left_elbow'), ('left_elbow', 'left_wrist'), ('left_hip', 'left_knee'), ('left_knee', 'left_ankle'), ('left_ankle', 'left_foot_index'), ('forehead', 'torso')]

    def calculate_additional_columns(kd):
        kd.loc[:, 'forehead_x'] = (kd['left_eye_outer_x'] + kd['right_eye_outer_x']) / 2
        kd.loc[:, 'forehead_y'] = (kd['left_eye_outer_y'] + kd['right_eye_outer_y']) / 2
        kd.loc[:, 'forehead_z'] = (kd['left_eye_outer_z'] + kd['right_eye_outer_z']) / 2

        kd.loc[:, 'torso_x'] = (kd['left_shoulder_x'] + kd['right_shoulder_x'] + kd['left_hip_x'] + kd['right_hip_x']) / 4
        kd.loc[:, 'torso_y'] = (kd['left_shoulder_y'] + kd['right_shoulder_y'] + kd['left_hip_y'] + kd['right_hip_y']) / 4
        kd.loc[:, 'torso_z'] = (kd['left_shoulder_z'] + kd['right_shoulder_z'] + kd['left_hip_z'] + kd['right_hip_z']) / 4

        for joint in joint_pairs:
            angles = []
            distances = []
            velocities = []
            for i in range(len(kd)):
                joint1 = np.array([kd[f"{joint[0]}_x"].iloc[i], kd[f"{joint[0]}_y"].iloc[i], kd[f"{joint[0]}_z"].iloc[i]])
                joint2 = np.array([kd[f"{joint[1]}_x"].iloc[i], kd[f"{joint[1]}_y"].iloc[i], kd[f"{joint[1]}_z"].iloc[i]])
                dot_product = np.dot(joint1, joint2)
                magnitude1 = np.linalg.norm(joint1)
                magnitude2 = np.linalg.norm(joint2)
                distance = np.linalg.norm(joint1 - joint2)
                angle = np.degrees(np.arccos(dot_product / (magnitude1 * magnitude2)))
                angles.append(angle)
                distances.append(distance)

                if i == 0:
                    velocity = 0
                    velocities.append(velocity)
                else:
                    velocity = (distances[i] - distances[i-1]) * fps
                    velocities.append(velocity)

            kd[f"a_{joint[0]}_{joint[1]}"] = angles
            kd[f"d_{joint[0]}_{joint[1]}"] = distances
            kd[f"v_{joint[0]}_{joint[1]}"] = velocities

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            kd = pd.read_csv(f'{input_dir}/{filename}')
            fps = int(kd['fps'][0])
            kd = kd[::fps].reset_index(drop=True)
            calculate_additional_columns(kd)
            filename_without_ext = filename.split('.')[0]
            kd.to_csv(f'./data/processed/{filename_without_ext}.csv')
            print(f'{filename_without_ext} has been processed!')