import cv2
import time
import os



def save_frame(frame, frame_count):
    height, width = frame.shape[:2]
    bottom_third_with_offset = frame[int(height * 2 / 3)+40 :height, :]
    save_path = os.path.join("./output", f"frame_{frame_count}.jpg")
    cv2.imwrite(save_path, bottom_third_with_offset)
    print("Frame saved at:", save_path)
def process_frame(frame, frame_count, last_save_time):
    if frame is None:
        print("Error: Frame is None.")
        return
    
    # Split the frame into B, G, R channels
    b, g, r = cv2.split(frame)
    
    # Check the green channel value at the specified coordinates
    green_value = g[693,644]  # Assuming the coordinates are within the frame dimensions
    blue_value = b[693,644] # THIS IS Y,X
    red_value = r[693,644]
    print("Green channel value at specified coordinates:", green_value)
    print("Blue channel value at specified coordinates:", blue_value)
    print("Red channel value at specified coordinates:", red_value)
    print("\n")
    # Check if the green channel value is not 19
    if green_value == 246 or green_value == 247 or green_value==249:
        # Check if it's been more than 2 seconds since the last save
        current_time = time.time()
        if current_time - last_save_time >= 2:
            # Perform your action here
            print("Green channel value is not 19. Performing action...")
            # For example, save the frame
            save_frame(frame, frame_count)
            return current_time  # Return the current time
    return last_save_time

# Open the video file
cap = cv2.VideoCapture('./videos/vid.mp4')

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

frame_count = 0  # Initialize frame count
last_save_time = time.time()  # Initialize last save time
# Loop through each frame
while cap.isOpened():
    ret, frame = cap.read()  # Read the frame
    if not ret:
        break
    # Display the frame
    cv2.imshow('Video', frame)
    # Process the frame
    last_save_time = process_frame(frame, frame_count, last_save_time)
    frame_count += 1  # Increment frame count
    
    key = cv2.waitKey(25)
    if key == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()