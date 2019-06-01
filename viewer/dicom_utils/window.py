import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


class DicomImageDisplay:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.image_id = None
        self.original_image = None
        self.window_width = None
        self.window_centre = None
        self.root = root
        self.image = None

        self.prev_coords = None

    def set_default_image(self):
        array_img = np.ndarray(self.canvas_dimensions())
        color = 255
        array_img.fill(color)
        self.original_image = array_img
        self.image = self._np_array_to_image(array_img)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def set_image(self, image, window_width, window_centre):
        self.original_image = image
        self.set_window_params(window_width, window_centre)
        self._update_image()

    def set_window_params(self, window_width=None, window_centre=None):
        if window_width is not None:
            self.window_width = window_width
        if window_centre is not None:
            self.window_centre = window_centre
        self._update_image()

    def update_window_params(self, event):
        x, y = event.x, event.y
        if self.prev_coords is None and event.type == '4' and event.num == 1:
            self.prev_coords = (x, y)
        elif self.prev_coords is not None:
            new_params = self._coords_to_window_params((x, y))
            self.set_window_params(*new_params)
            if event.type == '5' and event.num == 1:
                self.prev_coords = None
            else:
                self.prev_coords = (x, y)

    def _coords_to_window_params(self, coords):
        dx = coords[0] - self.prev_coords[0]
        dy = coords[1] - self.prev_coords[1]
        return max(1, self.window_width + 5 * dx), max(1, self.window_centre + 5 * dy)

    def _update_image(self):
        windowed_image = self.apply_window(self.original_image)
        self.image = self._np_array_to_image(windowed_image)
        self.canvas.itemconfig(self.image_id, image=self.image)

    def _np_array_to_image(self, img):
        image = Image.fromarray(img).resize(self.canvas_dimensions())
        imagetk = ImageTk.PhotoImage(image=image)
        return imagetk

    def _map_pixel(self, pixel, window_width, window_centre):
        if pixel < window_centre - window_width / 2.0:
            return 0.0
        if pixel > window_centre + window_width / 2.0:
            return 255.0
        return (pixel - window_centre + window_width / 2.0) / window_width * 255.0

    def apply_window(self, image):
        img = np.ndarray(image.shape)
        for i in range(len(image)):
            for j in range(len(image[i])):
                img[i][j] = self._map_pixel(image[i][j], self.window_width, self.window_centre)
        return img

    def canvas_dimensions(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()






