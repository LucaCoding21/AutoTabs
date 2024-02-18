import cv2
import time
import os



def save_frame(frame, frame_count):
    height, width = frame.shape[:2]
    bottom_third_with_offset = frame[int(height * 2 / 3) - 50:height, :]
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
    green_value = g[619, 1179]  # Assuming the coordinates are within the frame dimensions
    print("Green channel value at specified coordinates:", green_value)
    
    # Check if the green channel value is not 19
    if green_value == 47 or green_value == 48 or green_value == 46:
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
cap = cv2.VideoCapture('./images/vid.mp4')

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get the frame width and height
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Print coordinates of top-right and bottom-left pixels
top_right = (width - 1, 0)
bottom_left = (0, height - 1)
print("Top right coordinate:", top_right)
print("Bottom left coordinate:", bottom_left)

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
