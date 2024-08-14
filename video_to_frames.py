import cv2
import os
import numpy as np

# Path to the video file
video_path = 'path/to/your/video.mp4'
# Directory to save the frames
output_dir = 'path/to/store/frames'
os.makedirs(output_dir, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the frame rate and total number of frames
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}")
print(f"Total Frames: {total_frames}")

# Start time in seconds (7 minutes)
start_time = 7 * 60
start_frame = int(fps * start_time)

print(f"Start Frame: {start_frame}")

# Ensure start_frame is within the video range
if start_frame >= total_frames:
    print("Start frame is beyond the end of the video.")
    exit()

# Set the video position to the starting frame
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# Verify the current position
current_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
print(f"Current Position (should be start_frame): {current_pos}")

# Initialize variables for scene detection
prev_frame = None
frame_count = 0
threshold = 30  # Adjust this value to control sensitivity

def calculate_frame_difference(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Calculate absolute difference between frames
    diff = cv2.absdiff(gray1, gray2)
    
    # Calculate mean difference
    mean_diff = np.mean(diff)
    
    return mean_diff

# Loop through the frames starting from 00:07:00
while True:
    # Read the next frame
    ret, frame = cap.read()
    
    # If the frame was read correctly, ret is True
    if not ret:
        break
    
    # If it's the first frame, save it and continue
    if prev_frame is None:
        prev_frame = frame
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:06d}.jpg')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
        continue
    
    # Calculate difference with previous frame
    diff = calculate_frame_difference(prev_frame, frame)
    
    # If the difference is above the threshold, save the frame
    if diff > threshold:
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:06d}.jpg')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
        prev_frame = frame

# Release the video capture object
cap.release()
print(f'Extracted {frame_count} frames from 00:07:00 to the end of the video.')