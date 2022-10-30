import time
import typing as tp
import math
import random

import cv2
from matplotlib import pyplot as plt
from scipy.special import comb
import numpy as np
from collections import namedtuple


Point = namedtuple('Point', ('x', 'y'))

C = 0.551915024494
# (1, 0), (c, 1), (1, c), (0, 1) ()
# But to randomize it's more convinient to work with polar points
B = math.atan(C)
D = math.sqrt(math.pow(C, 2) + 1)

# And we want to remove the last point from quarter to join with other quarters
PERFECT_QUARTER_POINTS = np.array([(1, 0), (D, B), (D, math.pi / 2 - B)])
QUARTER_ANGLE = math.pi / 2


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


def calculate_mask(xvals: np.array, yvals: np.array, image_shape: np.ndarray) -> np.ndarray:
    assert len(image_shape) == 2
    _xvals, _yvals = xvals.copy(), yvals.copy()
    result = np.zeros(image_shape)
    xmin, xmax = np.min(_xvals), np.max(_xvals)
    ymin, ymax = np.min(_yvals), np.max(_yvals)
    width, height = xmax - xmin, ymax - ymin
    target_width, target_height = image_shape
    xscale, yscale = (target_width) / width, (target_height) / height
    middle_rate = random.uniform(0.8, 1)
    scale = min([xscale, yscale]) * middle_rate
    _xvals -= xmin
    _yvals -= ymin
    _xvals *= scale
    _yvals *= scale
    _xvals += target_width * (1 - middle_rate) * .5
    _yvals += target_height * (1 - middle_rate) * .5
    _xvals[_xvals >= image_shape[0]] = image_shape[0] - 1
    _yvals[_yvals >= image_shape[1]] = image_shape[1] - 1
    _xvals = _xvals.astype(np.int)
    _yvals = _yvals.astype(np.int)
    _vals = np.column_stack((_yvals, _xvals))
    # Fastest way to put a value in array with a given list of indexes
    np.put(result, np.ravel_multi_index(_vals.T, result.shape), 1)
    return result


def show_image(img: np.array):
    plt.imshow(img, cmap='gray')
    plt.show()


def rotate(image: np.array, rho: float, scale: float):
    rotation = max([random.randint(0, int(rho * 360)), 1])
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rotated_mask_circle = cv2.getRotationMatrix2D(image_center, rotation, scale)
    return cv2.warpAffine(image, rotated_mask_circle, image.shape[1::-1], flags=cv2.INTER_LINEAR)
