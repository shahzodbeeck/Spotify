import cv2
import numpy as np


def euclidean_distance(color1, color2):
    return np.linalg.norm(np.array(color1[:3]) - np.array(color2[:3]))


def get_average_color(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape((-1, 3))
    average_color = np.mean(pixels, axis=0)
    return [int(val) for val in average_color] + [1]


