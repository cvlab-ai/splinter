from PIL import Image
from os import listdir
from os.path import splitext
import sys
import shutil

from tqdm import tqdm

from utils import *


Path("extract").mkdir(parents=True, exist_ok=True)
Path("rotate").mkdir(parents=True, exist_ok=True)
Path("anonymize").mkdir(parents=True, exist_ok=True)

target_directory = sys.argv[1] if len(sys.argv) > 1 else '.'

image_exts = ['.png', '.jpg']
pdf_exts = ['.pdf']
target_ext = '.png'

print(f"Starting... (target directory: {target_directory})")

for file in tqdm(sorted(listdir(target_directory))):
  print("Image: ", file)
  filename, ext = splitext(file)
  try:
    if ext in image_exts:
      im = Image.open(f"{target_directory}/{filename}{ext}")
      im.save(f'extract/{filename}{target_ext}')
    if ext in pdf_exts:
      pages = convert_from_path(f"{target_directory}/{filename}{ext}")
      for i, page in enumerate(pages):
        page.save(f'extract/{filename}_page_{i}{target_ext}')
  except OSError:
    print('Cannot convert %s' % file)

print("Files extracted")

# rotation
for file in tqdm(sorted(listdir('./extract'))):
  print("Image:", file)
  img = cv2.imread(f"extract/{file}") # load image
  try:
    contours = detect_black_squares(img) # detect squares

    # calculate angle for each square
    angles = []

    for _, contour in contours:
      _angle = detect_rotation_angle(contour)
      angles.append(_angle)

    if any(i < 5 for i in angles) and any(i > 85 for i in angles):
      for i, angle in enumerate(angles):
        if angle < 5:
          angles[i] += 90.0


    angle = np.average(angles) # calculating the final offset as an average
    
    if any(abs(angles[i] - angles[i + 1]) > 10.0 for i in range(len(angles) - 1)):
      angle = 0.0

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

    cv2.imwrite(f"rotate/{file}", img)
  except Exception as e:
    print(f"Skipping {file} file due to following error: {e}. Saving original file...")
    img = cv2.imread(f"extract/{file}")
    cv2.imwrite(f"anonymize/{file}", img)

print("Files rotated")

# anonymization
for file in tqdm(sorted(listdir('./rotate'))):
  print("Image:", file)
  img = cv2.imread(f"rotate/{file}")

  detect_student_name(img)

  cv2.imwrite(f"anonymize/{file}", img)

print("Cleaning...")

shutil.rmtree("./extract")
shutil.rmtree("./rotate")