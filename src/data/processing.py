import os
import cv2
import pandas as pd
import warnings
from sklearn.ensemble import IsolationForest

def create_output_dir_if_not_exists(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def process_landmarks_using_isolation_forest(input_dir: str):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        output_dir = "data/processed/"
        create_output_dir_if_not_exists(output_dir)
        for subdir, dirs, files in os.walk(input_dir):
            for file in files:
                if file == "landmarks_rel.csv":
                    input_file_path = os.path.join(subdir, file)
                    output_file_path = os.path.join(output_dir, os.path.basename(subdir) + ".csv")
                    kinematic_data = pd.read_csv(input_file_path)
                    clf = IsolationForest(contamination=0.1)
                    clf.fit(kinematic_data)
                    outliers = pd.Series(clf.predict(kinematic_data))
                    kinematic_data['is_outlier'] = outliers
                    filtered_kinematic_data = kinematic_data[outliers == 1]

                    create_output_dir_if_not_exists(os.path.dirname(output_file_path))
                    filtered_kinematic_data.to_csv(output_file_path, index=False)
                    print(f"Processed {input_file_path} and saved results to {output_file_path}")

def check_video_size(video_path):
    video_size = None
    for filename in os.listdir(video_path):
        if filename.endswith('.mp4'):
            filepath = os.path.join(video_path, filename)
            cap = cv2.VideoCapture(filepath)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            if video_size is None:
                video_size = (width, height)
            elif (width, height) != video_size:
                return False
    return True