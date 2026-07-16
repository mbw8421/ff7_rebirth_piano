import cv2
import numpy as np

def preprocess_for_change_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Rescale the image to be larger
    gray = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    return binary


video_path = 'songs/FF7 Rebirth All Piano Sheet Music S-Ranked Gameplay.mp4'
cap = cv2.VideoCapture(video_path)

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)


def frame_to_timestamp(frame_number):
    # Calculate the total seconds for the given frame number
    total_seconds = frame_number / float(fps)

    # Calculate hours, minutes, and seconds
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    # Calculate milliseconds more accurately
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)

    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"


# Define the start and stop times in seconds
start_time = 286
stop_time = 384

# Convert start and stop times to frame numbers
start_frame = start_time * fps
stop_frame = stop_time * fps

# Set the starting frame of the video
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

x, y, w, h = 185, 53, 55, 29  # Example values

# frame_count = start_frame
change_count = 0
last_change_frame = 0

ret, prev_frame = cap.read()
roi = prev_frame[y:y + h, x:x + w]
prev_frame_roi = preprocess_for_change_detection(roi)

while True:
    # Get the current frame number
    current_frame_no = cap.get(cv2.CAP_PROP_POS_FRAMES)

    # Stop the loop if we've gone beyond the stop_frame
    if current_frame_no > stop_frame:
        break

    ret, current_frame = cap.read()
    # frame_count += 1
    if not ret:
        break

    # if frame_count % 3 != 0:
    #     continue

    roi = current_frame[y:y + h, x:x + w]
    current_frame_roi = preprocess_for_change_detection(roi)

    # Compute absolute difference between the previous frame and the current frame
    frame_delta = cv2.absdiff(prev_frame_roi, current_frame_roi)
    change_level = np.sum(frame_delta)

    # If change_level is above a threshold, a change occurred
    if change_level > 200_000 and current_frame_no - last_change_frame > 12:
        change_count += 1
        last_change_frame = current_frame_no
        print(f"{change_count} {change_level} Change detected. {frame_to_timestamp(current_frame_no)}")
        # Debug: show the frame on which we're detecting changes
        cv2.imshow('Frame Delta', roi)
        cv2.waitKey(0)

    # Update the previous frame
    prev_frame_roi = current_frame_roi

cap.release()
cv2.destroyAllWindows()
