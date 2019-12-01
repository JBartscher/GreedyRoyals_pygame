import math

import numpy as np


def calculate_center_point(max_x: int, max_y: int):
    """
    calculates the center of sth. and returns it as a point/ numpy array.

    :return: the center point which of the range given from width and height
    """
    w = int(max_x / 2)
    h = int(max_y / 2)
    return np.array([int(max_x / 2), int(max_y / 2)])


def transform_coordinate_array_to_homogeneous_translation_matrix(coordinates: np.array):
    """
    transforms a numpy array into a homogeneous translation matrix.

                 [1, 0, x]
    [x, y]  -->  [0, 1, y]
                 [0, 0, 1]

    :param coordinates: regular coordinate numpy array
    :return: a homogeneous translation matrix depicted through a numpy array
    """
    return np.array([[1, 0, coordinates[0]], [0, 1, coordinates[1]], [0, 0, 1]])


def transform_homogeneous_coordinates_to_coordinate_array(coordinates: np.array):
    """
    transforms homogeneous coordinates to regular coordinates.

    :param coordinates: homogeneous coordinates
    :return: regular coordinate numpy array
    """
    return np.array([coordinates[0][0], coordinates[1][0]])


def transform_coordinate_array_to_homogeneous_coordinates(coordinates: np.array):
    """
     transforms a numpy array into a homogeneous coordinates (coordinates ∈ R²).

                 [x]
    [x, y]  -->  [y]
                 [1]

    :param coordinates: numpy array of (length 2) with two values that represent x and y
    :return: homogeneous coordinate numpy array
    """
    return np.array([[coordinates[0]], [coordinates[1]], [1]])


def translate_coordinates(a, b):
    """
    takes two np.arrays (NOT YET HOMOGENEOUS!) (a,b ∈ R²) and translates a with b.

    [a_x]       [1, 0, x]   [x]
    [a_y]  *    [0, 1, y] = [y]
    [1]         [0, 0, 1]   [1]

    :param b: a regular coordinate numpy array
    :param a: a regular coordinate numpy array
    :return: translated regular coordinates
    """
    v = transform_coordinate_array_to_homogeneous_coordinates(a)
    m = transform_coordinate_array_to_homogeneous_translation_matrix(b)

    return transform_homogeneous_coordinates_to_coordinate_array(m.dot(v))


def normal_vector(u, v, norm=1):
    """
    gets the normal vector between two vectors and normalizes it.

    :param u: vector depicted by a numpy array
    :param v: vector depicted by a numpy array
    :param norm:
    :return: the normal vector btween two vectors
    """
    _ = np.cross(transform_coordinate_array_to_homogeneous_coordinates(v),
                 transform_coordinate_array_to_homogeneous_coordinates(u), axis=0)
    return transform_homogeneous_coordinates_to_coordinate_array(_)


def normalize_vector(v, norm=1):
    """
    normalize a vector.

    :param v: vector depicted by a numpy array
    :param norm: norm by which the vector is normalized
    :return: the normalized vector by the norm
    """
    length = np.math.sqrt(v[0] ** 2 + v[1] ** 2)
    scalar = norm / length
    return np.around(v * scalar, decimals=3)


def calculate_vector_angle_in_degree(v):
    """
    calculates the current direction in degrees from x-axis. Rounds the result to 2 digits after the comma.
    :return: angle in degrees
    """
    # u=np.array([1, 0])
    # dot = u[0] * v[0] + u[1] * v[1]  # dot product
    # det = u[0] * v[1] - u[1] * v[0]  # determinant

    # rad = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    rad = math.atan2(v[1], v[0])

    # negative angle => bigger than 180°
    angle = round(math.degrees(rad), 2)
    if angle < 0:
        angle = angle + 360

    return angle


def compare_2d_array(v, u):
    """
    compare 2 numpy 2 dimensional arrays without decimals.

    :param v: first numpy array
    :param u: second numpy array
    :return: True if equal otherwise False
    """
    v = np.around(v, 0)
    u = np.around(u, 0)
    return v[0] == u[0] and v[1] == u[1]


def mirror_at_half_by_x_axis(v, y_max):
    """
    mirrors the point at half of screen (y_max) by x-axis

    :param v: the point that gets translated
    :param y_max: max height of pane
    :return: the mirrored coordinates
    """
    mT = -1 * np.array([0, y_max / 2])
    v = translate_coordinates(v, mT)
    v[1] = v[1] * -1
    mT = np.array([0, y_max / 2])
    v = translate_coordinates(v, mT)

    return v


def calculate_relative_degree(v, u):
    """
    calculates the relative degree between two vectors

    :param v: first vector
    :param u: second vector
    :return: degree between those two vectors
    """
    v = translate_coordinates(v, -1 * u)
    return calculate_vector_angle_in_degree(v, u)
