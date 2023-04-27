import os
import cv2

def save_mp4_to_frames(input_video_path: str, output_frames_dir: str):
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)

    cap = cv2.VideoCapture(input_video_path)
    frame_count = 0

    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        
        screenshot_path = os.path.join(output_frames_dir, f"{frame_count:05d}.png")
        cv2.imwrite(screenshot_path, image)
        frame_count += 1

    cap.release()
    return print(f"Saved {frame_count} frames to {output_frames_dir}.")