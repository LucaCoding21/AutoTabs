import cv2
import time
import os
from skimage.metrics import structural_similarity as ssim

# Function to save the frame
def save_frame(frame, frame_count):
    height, width = frame.shape[:2]
    bottom_third_with_offset = frame[int(height * 2 / 3) + 50:height, :]
    save_path = os.path.join("./output", f"frame_{frame_count}.jpg")
    cv2.imwrite(save_path, bottom_third_with_offset)
    print("Frame saved at:", save_path)

cap = cv2.VideoCapture('./videos/vid.mp4')

# Read the first frame
ret, first_frame = cap.read()


save_frame(first_frame, 0)

# Release the video capture object
cap.release()


# Function to process the frame
def process_frame(frame, prev_frame_roi, frame_count, last_save_time):
    if frame is None:
        print("Error: Frame is None.")
        return last_save_time, prev_frame_roi

    # Define the region of interest (ROI) coordinates
    top_left = (116, 644)  # Example coordinates, adjust as needed
    bottom_right = (1261, 681)  # Example coordinates, adjust as needed
    
    # Extract the region of interest (ROI) from the frame
    roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Convert the ROI to grayscale
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Convert ROI to binary image (black and white)
    _, roi_binary = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
    
    # Compare the current ROI with the previous one
    if prev_frame_roi is not None:
        # Calculate Structural Similarity Index (SSI) between current and previous ROI
        similarity_index = ssim(roi_binary, prev_frame_roi)
        if similarity_index < 0.95:  # Adjust the threshold as needed
            # If there's a significant change in the ROI, perform the action
            current_time = time.time()
            if current_time - last_save_time >= 0.1:
                print("Change detected in the region of interest. Performing action...")
                save_frame(frame, frame_count)
                last_save_time = current_time
                return last_save_time, roi_binary
    else:
        # For the first frame, set the previous ROI
        prev_frame_roi = roi_binary.copy()
    
    return last_save_time, roi_binary
# Open the video file
cap = cv2.VideoCapture('./videos/vid.mp4')

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

frame_count = 0  # Initialize frame count
last_save_time = time.time()  # Initialize last save time
prev_frame_roi = None  # Initialize previous ROI

# Set the frame skip count to process at x10 speed
frame_skip_count = 40

# Loop through each frame
while cap.isOpened():
    # Skip frames
    for _ in range(frame_skip_count):
        ret, frame = cap.read()  # Read the frame
        if not ret:
            break
    
    if not ret:
        break

    # Display the frame
    cv2.imshow('Video', frame)
    
    # Process the frame
    last_save_time, prev_frame_roi = process_frame(frame, prev_frame_roi, frame_count, last_save_time)
    frame_count += 1  # Increment frame count
    
    key = cv2.waitKey(25)
    if key == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()