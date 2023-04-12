import os
import time
import datetime

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

def datetime_str():
    now = datetime.datetime.now()
    datetime_str = now.strftime("%Y%m%d%H%M%S")
    return datetime_str

def date_str():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    return date_str