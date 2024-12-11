import glob
from PIL import Image, ImageDraw
import os
import random
import numpy as np
import math
import typing as tp
from scipy.special import comb
from tqdm import tqdm
# Get a list of all files matching the pattern
file_list = glob.glob('data/output/resized/*.jpg')

# Load all images from file_list
images = [Image.open(file) for file in file_list]

# Apply random marks to all images
for i, image in tqdm(enumerate(images)):
    os.makedirs(f'data/output/empty/{i}', exist_ok=True)
    for j in tqdm(range(250)):
        image.save(f'data/output/empty/{i}/unmarked_{j}.jpg')
