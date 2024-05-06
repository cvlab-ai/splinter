from pdf2image import convert_from_path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint
from pathlib import Path


def detect_black_squares(image):
  """
  Detect all black squares in the image
  Detection is based on detecting all squares,
  then selecting the largest one (max area)
  and filtering those that are similar to it.
  """
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

  edged = cv2.Canny(binary, 30, 200)

  contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  black_square_coords = []
  for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      ratio = float(w/h)
      if ratio >= 0.95 and ratio <= 1.05: # +/- 5%
        black_square_coords.append((w * h, contour))
  black_square_coords.sort(key=lambda x: x[0], reverse=True)
  reference_area = black_square_coords[0][0]

  filtered_squares = [square for square in black_square_coords if abs(square[0] - reference_area) <= 0.05 * reference_area] # +/- 5%
  return filtered_squares


def detect_rotation_angle(contour):
  """
  Ratation detection
  Checking by what angle the image should be rotated
  so that the square is parallel to the edge
  """
  rect = cv2.minAreaRect(contour)
  angle = rect[2]
  return angle if angle < 90.0 else angle - 90.0


def rotate_image(image, angle):
  """
  Rotate the image by a given angle
  """
  size_reverse = np.array(image.shape[1::-1]) # swap x with y
  M = cv2.getRotationMatrix2D(tuple(size_reverse / 2.), angle, 1.)
  MM = np.absolute(M[:,:2])
  size_new = MM @ size_reverse
  M[:,-1] += (size_new - size_reverse) / 2.
  return cv2.warpAffine(image, M, tuple(size_new.astype(int)), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def check_horizontal_line(squares, bottom_left_square):
  """
  Check the number of squares in a horizontal line to a given square
  """
  count = 0
  if bottom_left_square:
    _, y, _, h = bottom_left_square
    m = y + (h / 2)
    for square in squares:
      s_m = square[1] + (square[3] / 2)
      if m - 2 * h <= s_m <= m + 2 * h:
        count += 1
  return count

def check_vertical_line(squares, bottom_left_square):
  """
  Check the number of squares in a vertical line to a given square
  """
  count = 0
  if bottom_left_square:
    x, _, w, _ = bottom_left_square
    m = x + (w / 2)
    for square in squares:
      s_m = square[0] + (square[2] / 2)
      if m - 2 * w <= s_m <= m + 2 * w:
        count += 1
  return count

def find_bottom_left_square(squares, image):
  """
  Find left bottom square
  """
  height, _, _ = img.shape
  nearest_square = None
  min_distance = float('inf')
  for square in squares:
      x, y, _, _ = square
      distance = ((0 - x) ** 2 + (height - y) ** 2) ** 0.5
      if distance < min_distance:
          min_distance = distance
          nearest_square = square
  return nearest_square

def find_extreme_squares(squares, image):
  """
  Find the square closest to the top left
  and bottom right corners of the image
  """
  nearest_square = None
  farest_square = None
  min_distance = float('inf')
  max_distance = float('-inf')
  for square in squares:
      x, y, _, _ = square
      distance = x + y # L1
      if distance < min_distance:
          min_distance = distance
          nearest_square = square
      if distance > max_distance:
          max_distance = distance
          farest_square = square
  return nearest_square, farest_square


def detect_student_name(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

  edged = cv2.Canny(binary, 30, 200)

  contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  original_ratio = float(870 / 100) # hardcoded ratio based on sheet
  squares = []
  for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      ratio = float(w / h)
      if 0.8 * ratio <= original_ratio <= 1.2 * ratio:
        squares.append((w * h, (x, y, w, h)))

  squares.sort(key=lambda x: x[0], reverse=True)

  # find the pair of largest rectangles that fit the ratio
  similar_rectangles = None
  largest_area_difference = float('inf')

  for i in range(len(squares)):
      for j in range(i + 1, len(squares)):
          if 0.9 * squares[i][0] <= squares[j][0] <= 1.1 * squares[i][0]:
              area_difference = abs(squares[i][0] - squares[j][0])
              if area_difference < largest_area_difference:
                  similar_rectangles = (squares[i][1], squares[j][1])
                  largest_area_difference = area_difference

  # take the square that is lower than the other one
  rectangle = similar_rectangles[0] if similar_rectangles[0][1] > similar_rectangles[1][1] else similar_rectangles[1]
  assert rectangle is not None

  # put the mask on the rectangle
  x, y, w, h = rectangle
  image = cv2.rectangle(
    image,
    (x, y),
    (x + w, y + h),
    (255, 255, 255),
    -1
  )

  return rectangle