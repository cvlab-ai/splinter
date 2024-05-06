from pdf2image import convert_from_path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint
from pathlib import Path
import sys
import tqdm


Path("extract").mkdir(parents=True, exist_ok=True)
Path("rotate").mkdir(parents=True, exist_ok=True)
Path("anonymize").mkdir(parents=True, exist_ok=True)

file_name = sys.argv[1]

pages = convert_from_path(file_name, 300)

# extraction
for i, page in tqdm(enumerate(pages)):
  page.save(f'extract/{i}.png')

# rotation
for i in range(len(pages)):
  print("Image:", i)
  img = cv2.imread(f"extract/{i}.png") # load image

  contours = detect_black_squares(img) # detect squares

  # calculate angle for each square
  angles = []
  for _, contour in contours:
    _angle = detect_rotation_angle(contour)
    angles.append(_angle)

  angle = np.average(angles) # calculating the final offset as an average
  print("Angle:", angle, angles)
  img = rotate_image(img, angle) # rotate image
  contours = detect_black_squares(img) # detect squares again (after rotation)

  squares = []
  for _, contour in contours:
    squares.append(cv2.boundingRect(contour))

  bottom_left_square = find_bottom_left_square(squares, img)
  horizontal = check_horizontal_line(squares, bottom_left_square)
  vertical = check_vertical_line(squares, bottom_left_square)

  nearest, farest = find_extreme_squares(squares, img)
  # crop image
  img = img[nearest[1] - nearest[3]:farest[1] + 2 * farest[3], nearest[0] - nearest[2]:farest[0] + 2 * farest[2]]

  # detect position based on pattern and rotate image
  if horizontal == 2 and vertical == 2:
    img = cv2.rotate(img, cv2.ROTATE_180)
  if horizontal == 3 and vertical == 2:
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
  if horizontal == 2 and vertical == 3:
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

  cv2.imwrite(f"rotate/{i}.png", img)

# anonymization
for i in range(len(pages)):
  print("Image:", i)
  img = cv2.imread(f"rotate/{i}.png")

  detect_student_name(img)

  cv2.imwrite(f"anonymize/{i}.png", img)