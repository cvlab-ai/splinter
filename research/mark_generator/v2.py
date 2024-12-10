from PIL import Image
import cv2
import numpy as np

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

# Get the center and area around each box
box_areas = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 10 and h > 10:  # Filter out small boxes
        center_x = x + w // 2
        center_y = y + h // 2
        area = gray_image[center_y-h:center_y+h, center_x-w:center_x+w]
        if center_y - h < 0 or center_y + h > gray_image.shape[0] or center_x - w < 0 or center_x + w > gray_image.shape[1]:
            padded_image = cv2.copyMakeBorder(gray_image, h, h, w, w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            center_y += h
            center_x += w
            w = int(w * 2 / 3)
            h = int(h * 2 / 3)
            area = padded_image[center_y-h:center_y+h, center_x-w:center_x+w]
        else:
            w = int(w * 2 / 3)
            h = int(h * 2 / 3)
            area = gray_image[center_y-h:center_y+h, center_x-w:center_x+w]
        try:
            cv2.imwrite(f'data/output/box_{center_x}_{center_y}.jpg', area)
        except:
            pass

# Example: Print the center and area shape of the first box
if box_areas:
    first_box = box_areas[0]
    print(f"Center of first box: (x = {first_box[0]}, y = {first_box[1]})")
    print(f"Area shape of first box: {first_box[2].shape}")