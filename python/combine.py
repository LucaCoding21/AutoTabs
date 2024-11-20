import cv2
import os

def extract_frame_number(filename):
    # Extract the frame number from the filename
    return int(filename.split('_')[1].split('.')[0])

def combine_images(image_folder, output_folder, frames_per_combination):
    # Get list of all files in the image folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    if not image_files:
        print("No JPG files found in the specified folder.")
        return
    
    # Sort the list of image files based on frame number
    image_files.sort(key=extract_frame_number)
    
    # Split the image files into groups based on frames_per_combination
    image_groups = [image_files[i:i + frames_per_combination] for i in range(0, len(image_files), frames_per_combination)]
    
    for i, image_group in enumerate(image_groups):
        images = []
        for image_file in image_group:
            # Read each image
            image_path = os.path.join(image_folder, image_file)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Unable to read image '{image_file}'.")
                continue
            
            images.append(image)
        
        if not images:
            print("No valid images found in the specified folder.")
            continue
        
        # Stack images vertically
        combined_image = cv2.vconcat(images)
        
        # Write the combined image to the output folder
        output_path = os.path.join(output_folder, f"combined_image_{i+1}.jpg")
        cv2.imwrite(output_path, combined_image)
        print(f"Combined image saved to {output_path}.")

# Specify the folder containing the cropped JPG images
image_folder = './output'

# Specify the output path for the combined image
output_folder = './images/'

# Specify the number of frames per combination
frames_per_combination = 4  # Adjust as needed

# Combine images
combine_images(image_folder, output_folder, frames_per_combination)
