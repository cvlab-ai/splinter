
import cv2
import numpy as np

from src.utils.exceptions import ExamNotDetected


def rotate_exam(image: np.ndarray):
    try:
        for _ in range(3):
            reference_points = detect_reference_points(image)

            image, angle = __rotate_to_right_angle(image, reference_points)

            if angle < 1e-5:
                break

        image = __rotate_to_vertical(image)

        return image
    except Exception as e:
        raise ExamNotDetected(e)

def detect_reference_points(image):
    """
    Detect all reference points in the image
    Detection is based on detecting all squares,
    then selecting the largest one (max area)
    and filtering those that are similar to it.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
        _, _, w, h = cv2.boundingRect(contour)
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


def __rotate_to_right_angle(image, reference_points):
    angles = []

    for _, contour in reference_points:
        _angle = __detect_rotation_angle(contour)
        angles.append(_angle)

    if any(i < 5 for i in angles) and any(i > 85 for i in angles):
        for i, angle in enumerate(angles):
            if angle < 5:
                angles[i] += 90.0


    angle = np.average(angles) # calculating the final offset as an average
    
    if any(abs(angles[i] - angles[i + 1]) > 10.0 for i in range(len(angles) - 1)):
      angle = 0.0

    return __rotate_image(image, angle), angle


def __detect_rotation_angle(contour):
    """
    Ratation detection
    Checking by what angle the image should be rotated
    so that the square is parallel to the edge
    """
    rect = cv2.minAreaRect(contour)
    angle = rect[2]
    
    return angle if angle < 90.0 else angle - 90.0


def __rotate_image(image, angle):
    """
    Rotate the image by a given angle
    """
    size_reverse = np.array(image.shape[1::-1]) # swap x with y
    M = cv2.getRotationMatrix2D(tuple(size_reverse / 2.), angle, 1.)
    MM = np.absolute(M[:,:2])
    size_new = MM @ size_reverse
    M[:,-1] += (size_new - size_reverse) / 2.
    return cv2.warpAffine(image, M, tuple(size_new.astype(int)), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def __rotate_to_vertical(image):
    """
    Turn the image vertically
    """
    contours = detect_reference_points(image)

    squares = []
    for _, contour in contours:
      squares.append(cv2.boundingRect(contour))

    bottom_left_square = __find_bottom_left_square(squares, image)
    horizontal = __check_horizontal_line(squares, bottom_left_square)
    vertical = __check_vertical_line(squares, bottom_left_square)

    # detect position based on pattern and rotate image
    if horizontal == 2 and vertical == 2:
        return cv2.rotate(image, cv2.ROTATE_180)
    if horizontal == 3 and vertical == 2:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    if horizontal == 2 and vertical == 3:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    return image

def __find_bottom_left_square(squares, image):
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


def __check_horizontal_line(squares, bottom_left_square):
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

def __check_vertical_line(squares, bottom_left_square):
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