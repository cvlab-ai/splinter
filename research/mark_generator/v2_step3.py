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
C = 0.551915024494
# (1, 0), (c, 1), (1, c), (0, 1) ()
# But to randomize it's more convinient to work with polar points
B = math.atan(C)
D = math.sqrt(math.pow(C, 2) + 1)

# And we want to remove the last point from quarter to join with other quarters
PERFECT_QUARTER_POINTS = np.array([(1, 0), (D, B), (D, math.pi / 2 - B)])
QUARTER_ANGLE = math.pi / 2

class Point(tp.NamedTuple):
    x: float
    y: float

def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * (t ** (n - i)) * (1 - t) ** i


def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1],
                 [2,3],
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals


def create_handwritten_circle(alpha: float, gamma: float):

    def create_next_quarter(last_quarter: np.array, _max_radius_dev: float, _max_angle_dev: float, close: bool = False):
        radius_deviation = random.normalvariate(0, _max_radius_dev / 3)
        angle_deviation = random.normalvariate(0, _max_angle_dev / 3)
        new_quarter = last_quarter.copy() + (radius_deviation, angle_deviation + QUARTER_ANGLE)
        if close:
            closing_point = last_quarter[0] + (radius_deviation, angle_deviation + 2 * QUARTER_ANGLE)
            new_quarter = np.append(new_quarter, [closing_point], axis=0)
        return new_quarter

    def pol2cart(radius: float, angle: float):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        return x, y

    max_radius_dev = random.normalvariate(0, alpha * 2)
    max_angle_dev = random.normalvariate(0, gamma * 4)

    quarters = [create_next_quarter(PERFECT_QUARTER_POINTS, max_radius_dev, max_angle_dev)]
    for quarter_number in range(3):  # add the remaining 3 quarters
        quarters.append(create_next_quarter(quarters[-1], max_radius_dev, max_angle_dev, quarter_number == 2))

    circle_point_pol = np.concatenate(quarters)
    circle_points_cart = np.array([pol2cart(radius, angle) for radius, angle in circle_point_pol])
    return bezier_curve(circle_points_cart, 10000)


def create_handwritten_cross(alpha: float, gamma: float):
    def generate_points(first_handle: tp.Tuple[float, float], control_point: tp.Tuple[float, float],
                        second_handle: tp.Tuple[float, float]):
        return [(first_handle[0] + random.normalvariate(0, alpha), first_handle[1] + random.normalvariate(0, alpha)),
                (control_point[0] + random.normalvariate(0, gamma), control_point[1] + random.normalvariate(0, gamma)),
                (second_handle[0] + random.normalvariate(0, alpha), second_handle[1] + random.normalvariate(0, alpha))]

    """
    :param alpha: deviation of start and end of the lines
    :param gamma: deviation from the center for the bezier control point
    """
    line1 = generate_points((0, 1), (.5, .5), (1, 0))
    line2 = generate_points((0, 0), (.5, .5), (1, 1))
    return np.concatenate((bezier_curve(line1, 10000), bezier_curve(line2, 10000)), axis=1)


def create_handwritten_doodle(alpha: float, beta: float, gamma: float, outlier_shape: tp.Tuple[float, float] = (1., 1.)):
    """
    :param alpha: deviation of handle points X values
    :param beta: deviation of handle points Y values
    :param gamma: deviation of bezier control point position
    """

    def calculate_control(first_handle: Point, second_handle: Point):
        middle_x, middle_y = abs(first_handle.x - second_handle.x) / 2, (
                    abs(first_handle.y - second_handle.y) / 2 + min(first_handle.y, second_handle.y))
        return random.normalvariate(middle_x, gamma), random.normalvariate(middle_y, 0)

    lines = []
    beta = max([beta / 4, 0.05])
    handlers = []
    recent_handle = Point(random.normalvariate(1 - outlier_shape[0], alpha / 6), random.normalvariate(1 - outlier_shape[1], beta / 6))
    i = 0
    while recent_handle.y < outlier_shape[1]:
        alpha_shift, beta_shift = random.normalvariate(0, alpha / 6), random.normalvariate(beta / 2, beta / 6)
        next_handle = Point(outlier_shape[0] + alpha_shift if i % 2 else 1 - outlier_shape[0] + alpha_shift,
                            recent_handle[1] + beta_shift)
        control_point = calculate_control(recent_handle, next_handle)
        lines.append(bezier_curve([recent_handle, control_point, next_handle], 10000))
        handlers.append(recent_handle)
        recent_handle = next_handle
        i += 1

    return np.concatenate(lines, axis=1)


def create_handwritten_tick(alpha: float, beta: float, gamma: float):
    left_handle = Point(random.normalvariate(0.1, alpha), random.normalvariate(0.1, beta))
    right_handle = Point(random.normalvariate(0.9, alpha), random.normalvariate(0.1, beta))
    right_control = Point(random.normalvariate(right_handle.x - gamma / 2, gamma / 6),
                          random.normalvariate(3 / 4, beta))
    left_control = Point(random.normalvariate(left_handle.x + gamma / 2, gamma / 6), random.normalvariate(3 / 4, beta))
    return bezier_curve([left_handle, right_control, left_control, right_handle], 1000)



def add_random_mark(image):

    def add_handwritten_mark(image, mark_type='doodle', alpha=random.uniform(0.03, 0.25), beta=random.uniform(0.03, 0.25), gamma=random.uniform(0.03, 0.25)):
        draw = ImageDraw.Draw(image)
        width, height = image.size
        x, y = width // 2, height // 2

        if mark_type == 'doodle':
            xvals, yvals = create_handwritten_doodle(alpha, beta, gamma)
        elif mark_type == 'cross':
            xvals, yvals = create_handwritten_cross(alpha, gamma)
        elif mark_type == 'circle':
            xvals, yvals = create_handwritten_circle(alpha, gamma)
        elif mark_type == 'tick':
            xvals, yvals = create_handwritten_tick(alpha, beta, gamma)
        else:
            raise ValueError(f"Unknown mark type: {mark_type}")

        xvals = (xvals * width).astype(int)
        yvals = (yvals * height).astype(int)

        # Center the mark on the image and scale it to 20-48 pixels
        mark_width = max(xvals) - min(xvals)
        mark_height = max(yvals) - min(yvals)
        scale_factor = random.uniform(20, 48) / max(mark_width, mark_height)

        xvals = ((xvals - min(xvals)) * scale_factor + x - (mark_width * scale_factor) / 2).astype(int)
        yvals = ((yvals - min(yvals)) * scale_factor + y - (mark_height * scale_factor) / 2).astype(int)

        steps = random.randint(2, 30)
        # Create a gradient of 10 random gray shades
        random_shades = np.random.normal(30, 200, steps).clip(0, 255).astype(int)
        gradient = np.interp(np.linspace(0, steps - 1, len(xvals)), np.arange(steps), random_shades).astype(int)
        gradient = [f'#{val:02x}{val:02x}{val:02x}' for val in gradient]
        for i in range(len(xvals) - 1):
            draw.line((xvals[i], yvals[i], xvals[i + 1], yvals[i + 1]), fill=gradient[i], width=2)

        # Odpowiedzi dookola
        cx = x
        cy = y
        for x, y in [(cx - 158, cy - 158), (cx, cy - 158), (cx + 158, cy - 158), (cx - 158, cy), (cx + 158, cy), (0, 158), (158, 158), (158, 158)]:
            if random.randint(1, 9) != 1:
                continue

            # odznaczenie
            mark_type = random.choice(['doodle', 'circle'])
            alpha = random.uniform(0.05, 0.2)
            beta = random.uniform(0.05, 0.2)
            gamma = random.uniform(0.05, 0.2)
            if mark_type == 'doodle':
                xvals, yvals = create_handwritten_doodle(alpha, beta, gamma)
            elif mark_type == 'circle':
                xvals, yvals = create_handwritten_circle(alpha, gamma)
            else:
                raise ValueError(f"Unknown mark type: {mark_type}")

            xvals = (xvals * width).astype(int)
            yvals = (yvals * height).astype(int)

            # Center the mark on the image and scale it to 20-48 pixels
            mark_width = max(xvals) - min(xvals)
            mark_height = max(yvals) - min(yvals)
            scale_factor = random.uniform(55, 80) / max(mark_width, mark_height)

            xvals = ((xvals - min(xvals)) * scale_factor + x - (mark_width * scale_factor) / 2).astype(int)
            yvals = ((yvals - min(yvals)) * scale_factor + y - (mark_height * scale_factor) / 2).astype(int)

            steps = random.randint(2, 30)
            # Create a gradient of 10 random gray shades
            random_shades = np.random.normal(30, 200, steps).clip(0, 255).astype(int)
            gradient = np.interp(np.linspace(0, steps - 1, len(xvals)), np.arange(steps), random_shades).astype(int)
            gradient = [f'#{val:02x}{val:02x}{val:02x}' for val in gradient]
            for i in range(len(xvals) - 1):
                draw.line((xvals[i], yvals[i], xvals[i + 1], yvals[i + 1]), fill=gradient[i], width=2)



        return image

    draw = ImageDraw.Draw(image)
    width, height = image.size
    mark_type = random.choice(['doodle', 'cross', 'tick'])

    return add_handwritten_mark(image, mark_type)

# Apply random marks to all images
for i, image in tqdm(enumerate(images)):
    os.makedirs(f'data/output/marked/{i}', exist_ok=True)
    for j in tqdm(range(3)):
        marked_image = add_random_mark(image.copy())
        marked_image.save(f'data/output/marked/{i}/marked_{j}.jpg')
