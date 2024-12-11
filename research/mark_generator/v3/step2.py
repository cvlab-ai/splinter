import glob
from PIL import Image
import os

# Get a list of all files matching the pattern
file_list = glob.glob('data/output/extract/box*.jpg')

def check_image_sizes(file_list):
    if not file_list:
        return True

    # Get the size of the first image
    with Image.open(file_list[0]) as img:
        first_image_size = img.size

    # Check the size of all other images
    for file in file_list[1:]:
        with Image.open(file) as img:
            print(img.size)
            if img.size != first_image_size:
                # Calculate the difference in dimensions
                width_diff = img.size[0] - first_image_size[0]
                height_diff = img.size[1] - first_image_size[1]

                # Crop the image to match the size of the first image
                left = 0 if width_diff <= 0 else width_diff // 2
                top = 0 if height_diff <= 0 else height_diff // 2
                right = img.size[0] if width_diff <= 0 else img.size[0] - width_diff // 2
                bottom = img.size[1] if height_diff <= 0 else img.size[1] - height_diff // 2

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img = cropped_img.resize(first_image_size)
                img = cropped_img
            if img.size != first_image_size:
                return False

    return True

# Check if all images have the same size
all_same_size = check_image_sizes(file_list)
print("All images have the same size:", all_same_size)

# Create the output directory if it doesn't exist
output_dir = 'data/output/resized'
os.makedirs(output_dir, exist_ok=True)

def save_resized_images(file_list, output_dir):
    if not file_list:
        return

    # Get the size of the first image
    with Image.open(file_list[0]) as img:
        first_image_size = img.size

    # Process and save all images
    for file in file_list:
        with Image.open(file) as img:
            if img.size != first_image_size:
                # Calculate the difference in dimensions
                width_diff = img.size[0] - first_image_size[0]
                height_diff = img.size[1] - first_image_size[1]

                # Crop the image to match the size of the first image
                left = 0 if width_diff <= 0 else width_diff // 2
                top = 0 if height_diff <= 0 else height_diff // 2
                right = img.size[0] if width_diff <= 0 else img.size[0] - width_diff // 2
                bottom = img.size[1] if height_diff <= 0 else img.size[1] - height_diff // 2

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img = cropped_img.resize(first_image_size)
                img = cropped_img

            # Save the resized image to the output directory
            output_path = os.path.join(output_dir, os.path.basename(file))
            img.save(output_path)

# Save all resized images
save_resized_images(file_list, output_dir)