import cv2

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Mouse clicked at (x={}, y={})".format(x, y))

# Open the video file
cap = cv2.VideoCapture('./videos/rom.mp4')

# Create a named window and set the mouse callback
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', on_mouse)

# Loop through each frame
while cap.isOpened():
    ret, frame = cap.read()  # Read the frame
    if not ret:
        break
    
    # Display the frame
    cv2.imshow('Video', frame)
    
    key = cv2.waitKey(25)
    if key == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
