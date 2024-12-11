from PIL import Image
import cv2
import numpy as np
import os

os.makedirs(f'data/output/', exist_ok=True)
os.makedirs(f'data/output/extract', exist_ok=True)
# Load the image
image_path = 'data/input/answer_boxes.jpg'
image = Image.open(image_path)

# Display the image (optional)
image.show()

# Convert the image to grayscale
gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

# Use Canny edge detection
edges = cv2.Canny(gray_image, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

box_sizes = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 10 and h > 10:  # Filter out small boxes
        box_sizes.append((w, h))

mean_width = np.mean([size[0] for size in box_sizes])
mean_height = np.mean([size[1] for size in box_sizes])
print(f"Mean box size: Width = {mean_width}, Height = {mean_height}")

# Find the smallest, largest, and middle y-coordinate in contours
y_coordinates = [cv2.boundingRect(contour)[1] for contour in contours if cv2.boundingRect(contour)[3] > 10 and cv2.boundingRect(contour)[2] > 10]
if y_coordinates:
    min_y = min(y_coordinates)
    max_y = max(y_coordinates)
    mid_y = np.median(y_coordinates)
    print(f"Smallest y-coordinate: {min_y}")
    print(f"Largest y-coordinate: {max_y}")
    print(f"Middle y-coordinate: {mid_y}")

# Get the center and area around each box
box_areas = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 10 and h > 10:  # Filter out small boxes
        if not (min_y - 0.1 * min_y <= y <= min_y + 0.1 * min_y or 
            max_y - 0.1 * max_y <= y <= max_y + 0.1 * max_y or 
            mid_y - 0.1 * mid_y <= y <= mid_y + 0.1 * mid_y):
            continue
        center_x = x + w // 2
        center_y = y + h // 2
        area = gray_image[center_y-h:center_y+h, center_x-w:center_x+w]
        if center_y - h < 0 or center_y + h > gray_image.shape[0] or center_x - w < 0 or center_x + w > gray_image.shape[1]:
            padded_image = cv2.copyMakeBorder(gray_image, h, h, w, w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            center_y += h
            center_x += w
            # w = int(w * 2 / 3)
            # h = int(h * 2 / 3)
            area = padded_image[center_y-h:center_y+h, center_x-w:center_x+w]
        else:
            # w = int(w * 2 / 3)
            # h = int(h * 2 / 3)
            area = gray_image[center_y-h:center_y+h, center_x-w:center_x+w]
        try:
            cv2.imwrite(f'data/output/extract/box_{center_x}_{center_y}.jpg', area)
        except:
            pass

# Example: Print the center and area shape of the first box
if box_areas:
    first_box = box_areas[0]
    print(f"Center of first box: (x = {first_box[0]}, y = {first_box[1]})")
    print(f"Area shape of first box: {first_box[2].shape}")