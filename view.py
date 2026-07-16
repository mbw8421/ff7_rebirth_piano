import cv2

video_path = 'songs/FF7 Rebirth All Piano Sheet Music S-Ranked Gameplay.mp4'
cap = cv2.VideoCapture(video_path)

# Enter the frame number where you want to check the ROI
frame_number_to_check = 17280
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number_to_check)

# Set the coordinates of the ROI (update these to your specific coordinates)
x, y, w, h = 185, 53, 55, 30  # Example values


ret, frame = cap.read()
if not ret:
    print("Failed to grab frame")
    cap.release()
    cv2.destroyAllWindows()
    exit()

roi = frame[y:y + h, x:x + w]

# Convert ROI to grayscale and threshold
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

# Draw a rectangle around the ROI
cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Show the frame with the ROI rectangle
cv2.imshow('ROI', binary)

# Extract the ROI and show it in a new window
# roi = frame[y:y+h, x:x+w]
# cv2.imshow('Extracted ROI', roi)

# Wait for a keypress to close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()
