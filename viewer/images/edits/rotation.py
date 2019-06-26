import math

import cv2


def rotate(image, angle):
    shape = (image.shape[1], image.shape[0])
    rotation_matrix = cv2.getRotationMatrix2D((shape[0] // 2, shape[1] // 2), angle, 1)
    return cv2.warpAffine(image, rotation_matrix, shape)


def flip(image, flip_type):
    return cv2.flip(image, flip_type)
