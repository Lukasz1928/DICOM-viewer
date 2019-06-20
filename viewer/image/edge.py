import numpy as np
import cv2


def canny(image):
    med = np.median(image)
    s = 0.33
    lower = int(max(0, (1 - s) * med))
    upper = int(max(0, (1 - s) * med))
    img = cv2.Canny(image, lower, upper)
    return img


def sobel(image):
    img = cv2.Sobel(image, -1, 1, 1, ksize=3)
    return img


def laplacian(image):
    img = cv2.Laplacian(image, -1, ksize=5)
    return img
