import cv2
import os

# Function to apply mask to an image
def apply_mask(image_path, output_path):
    print(f"Processing image: {image_path}")
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image {image_path}")
        return

    # Define the size of the mask
    mask_width = int(image.shape[1] * 0.25)  # Width of the mask (e.g., 25% of the image width)
    mask_height = image.shape[0]             # Full height of the image

    # Define the coordinates of the rectangle to mask
    start_point = (int(image.shape[1] * 0.87), 0)  # Start from 87% of the width
    end_point = (start_point[0] + mask_width, mask_height)  # Calculate the end point

    color = (255, 255, 255)  # White color
    thickness = -1           # Fill the rectangle

    # Apply the mask
    masked_image = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Save the modified image
    success = cv2.imwrite(output_path, masked_image)
    if success:
        print(f'Masked image saved to {output_path}')
    else:
        print(f"Error: Failed to save image to {output_path}")

def process_images_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            apply_mask(input_path, output_path)
        else:
            print(f"Skipped file (not an image): {filename}")

# Define the input and output directories
input_directory = 'path/to/extracted/frames_folder'
output_directory = 'path/to/store/crop_frames'

# Process all images in the directory
process_images_in_directory(input_directory, output_directory)