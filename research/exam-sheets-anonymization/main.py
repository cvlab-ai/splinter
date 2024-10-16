from PIL import Image
import glob
from os.path import splitext, dirname, isdir
import sys
import shutil
import re

from tqdm import tqdm

from utils import *

EXTRACT_DIR = "./extract"
ROTATE_DIR = "./rotate"


source_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
target_directory = sys.argv[2] if len(sys.argv) > 2 else './output'
filename_pattern = sys.argv[3] if len(sys.argv) > 3 else ""
logfile_pattern = sys.argv[4] if len(sys.argv) > 4 else "(txt|log)"

Path(EXTRACT_DIR).mkdir(parents=True, exist_ok=True)
Path(ROTATE_DIR).mkdir(parents=True, exist_ok=True)
Path(target_directory).mkdir(parents=True, exist_ok=True)

image_exts = ['.png', '.jpg']
pdf_exts = ['.pdf']
target_ext = '.png'

source_directory = source_directory.rstrip("\\/")
print("Starting...\nConfiguration:")
print(f"source directory: {source_directory}")
print(f"target directory: {target_directory}")
print(f"filename pattern: {filename_pattern}")
print(f"log file pattern: {logfile_pattern}")

for file in tqdm(glob.iglob(f"{source_directory}/**/*", recursive=True), desc="Creating structure"):
  filename, ext = splitext(file)
  filename = filename.removeprefix(source_directory)

  output_dir = f"{dirname(filename)}".rstrip("\\/")
  for dir in [EXTRACT_DIR, ROTATE_DIR, target_directory]:
    Path(f"{dir}/{output_dir}").mkdir(parents=True, exist_ok=True)

for file in tqdm(glob.iglob(f"{source_directory}/**/*", recursive=True), desc="Preprocessing"):
  if isdir(file):
    continue
  file = file.removeprefix(source_directory).lstrip("\\/").replace("\\", "/")

  filename, ext = splitext(file)

  if re.search(logfile_pattern, f"{filename}{ext}"):
    shutil.copy(f"{source_directory}/{filename}{ext}", f"{target_directory}/{filename}{ext}")

  if not re.search(filename_pattern, f"{filename}{ext}"):
    continue

  try:

    if ext in image_exts:
      im = Image.open(f"{source_directory}/{filename}{ext}")
      im.save(f'{EXTRACT_DIR}/{filename}{target_ext}')
    if ext in pdf_exts:
      pages = convert_from_path(f"{source_directory}/{filename}{ext}", dpi=300)
      for i, page in enumerate(pages):
        page.save(f'{EXTRACT_DIR}/{filename}_page_{i}{target_ext}')
  except OSError as e:
    print(e)
    print('Cannot convert %s' % file)

print("Files extracted")

# rotation
for file in tqdm(glob.iglob(f"{EXTRACT_DIR}/**/*", recursive=True), desc="Rotating"):
  if isdir(file):
    continue
  file = file.removeprefix(EXTRACT_DIR).lstrip("\\/")

  img = cv2.imread(f"{EXTRACT_DIR}/{file}") # load image
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

    cv2.imwrite(f"{ROTATE_DIR}/{file}", img)
  except Exception as e:
    print(f"Skipping {file} file due to following error: {e}. Saving original file...")
    img = cv2.imread(f"{EXTRACT_DIR}/{file}")
    cv2.imwrite(f"{target_directory}/{file}", img)

# anonymization
for file in tqdm(glob.iglob(f"{ROTATE_DIR}/**/*", recursive=True)):
  if isdir(file):
    continue
  file = file.removeprefix(ROTATE_DIR).lstrip("\\/")

  img = cv2.imread(f"{ROTATE_DIR}/{file}")

  detect_student_name(img)

  cv2.imwrite(f"{target_directory}/{file}", img)

print("Cleaning...")

shutil.rmtree(EXTRACT_DIR)
shutil.rmtree(ROTATE_DIR)