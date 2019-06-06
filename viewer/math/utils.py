import math

import numpy as np


def vector_length(vector):
    return np.linalg.norm(vector)


def vectors_angle(v1, v2):
    return math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def vectors_differ(v1, v2):
    return len(v1) != len(v2) or any([v1[i] != v2[i] for i in range(len(v1))])


def radians_to_degrees(radians):
    return 180.0 / math.pi * radians


def normalize_vector(vector):
    length = vector_length(vector)
    return tuple(float(x) / length for x in vector)


def points_to_vector(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]


def sum_vectors(v1, v2):
    return tuple(v1[i] + v2[i] for i in range(len(v1)))