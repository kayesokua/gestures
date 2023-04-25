import os
import time
import pandas as pd
from sklearn.ensemble import IsolationForest

def measure_elapsed_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.3f} seconds")
        return result
    return wrapper

def create_output_dir_if_not_exists(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def process_landmarks_using_isolation_forest(input_dir: str):
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