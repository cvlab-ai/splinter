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

  countours = []

  # adaptive threshold
  thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
  
  # Fill rectangular contours
  cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
      cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

  # Morph open
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

  contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  black_square_coords = []
  for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      ratio = float(w/h)
      approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True) 
      if ratio >= 0.95 and ratio <= 1.05 and len(approx) == 4: # +/- 5%
        black_square_coords.append((w * h, contour))
  black_square_coords.sort(key=lambda x: x[0], reverse=True)

  for i in range(len(black_square_coords)):
    reference_area = black_square_coords[i][0]

    filtered_squares = [square for square in black_square_coords if abs(square[0] - reference_area) <= 0.3 * reference_area] # +/- 30%
    if len(filtered_squares) == 6:
      return filtered_squares
  raise Exception("Couldn't find squares")


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
  height, _, _ = image.shape
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
  rectangles = []
  for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      ratio = float(w / h)
      if 0.8 * ratio <= original_ratio <= 1.2 * ratio:
        rectangles.append((w * h, (x, y, w, h)))

  rectangles.sort(key=lambda x: x[0], reverse=True)

  # find the pair of largest rectangles that fit the ratio
  similar_rectangles = None
  largest_area_difference = float('inf')

  for i in range(len(rectangles)):
    for j in range(i + 1, len(rectangles)):
      if 0.9 * rectangles[i][0] <= rectangles[j][0] <= 1.1 * rectangles[i][0]:
        similar_rectangles = (rectangles[i][1], rectangles[j][1])
        break
    if similar_rectangles is not None:
      break

  # take the square that is lower than the other one
  rectangle = similar_rectangles[0] if similar_rectangles[0][1] > similar_rectangles[1][1] else similar_rectangles[1]
  assert rectangle is not None
  print(rectangle)
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