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
    h, w = 360, 640
    joint_pairs = [('right_shoulder', 'right_elbow'), ('right_elbow', 'right_wrist'), ('right_hip', 'right_knee'), ('right_knee', 'right_ankle'), ('right_ankle', 'right_foot_index'), ('left_shoulder', 'left_elbow'), ('left_elbow', 'left_wrist'), ('left_hip', 'left_knee'), ('left_knee', 'left_ankle'), ('left_ankle', 'left_foot_index'), ('forehead', 'torso')]

    def calculate_additional_columns(df):
        df.loc[:, 'forehead_x'] = (df['left_eye_outer_x'] + df['right_eye_outer_x']) / 2
        df.loc[:, 'forehead_y'] = (df['left_eye_outer_y'] + df['right_eye_outer_y']) / 2
        df.loc[:, 'forehead_z'] = (df['left_eye_outer_z'] + df['right_eye_outer_z']) / 2

        df.loc[:, 'torso_x'] = (df['left_shoulder_x'] + df['right_shoulder_x'] + df['left_hip_x'] + df['right_hip_x']) / 4
        df.loc[:, 'torso_y'] = (df['left_shoulder_y'] + df['right_shoulder_y'] + df['left_hip_y'] + df['right_hip_y']) / 4
        df.loc[:, 'torso_z'] = (df['left_shoulder_z'] + df['right_shoulder_z'] + df['left_hip_z'] + df['right_hip_z']) / 4

        for joint in joint_pairs:
            angles = []
            distances = []
            for i in range(df.shape[0]):
                joint1 = df.loc[i, [f"{joint[0]}_x", f"{joint[0]}_y", f"{joint[0]}_z"]].to_numpy()
                joint2 = df.loc[i, [f"{joint[1]}_x", f"{joint[1]}_y", f"{joint[1]}_z"]].to_numpy()
                dot_product = np.dot(joint1, joint2)
                mag1 = np.linalg.norm(joint1)
                mag2 = np.linalg.norm(joint2)
                dist = np.linalg.norm(joint1 - joint2)
                angle = np.degrees(np.arccos(dot_product / (mag1 * mag2)))
                angles.append(angle)
                distances.append(dist)
            df[f"a_{joint[0]}_{joint[1]}"] = angles
            df[f"d_{joint[0]}_{joint[1]}"] = distances

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv') and not filename.endswith(('abs.csv', 'rel.csv')):
            kd_rel = pd.read_csv(f'{input_dir}/{filename}')
            kd_abs = kd_rel.copy()

            kd_abs.loc[:, kd_abs.columns.str.endswith('_x')] *= w
            kd_abs.loc[:, kd_abs.columns.str.endswith('_y')] *= h
            kd_abs.loc[:, kd_abs.columns.str.endswith('_z')] = h - kd_abs.loc[:, kd_abs.columns.str.endswith('_z')]

            calculate_additional_columns(kd_rel)
            calculate_additional_columns(kd_abs)

            filename_without_ext = filename.split('.')[0]

            kd_abs.to_csv(f'./data/processed/{filename_without_ext}_abs.csv', index=False)
            kd_rel.to_csv(f'./data/processed/{filename_without_ext}_rel.csv', index=False)
            print(f'{filename_without_ext} has been processed!')