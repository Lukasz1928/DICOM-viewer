import tkinter as tk

import numpy as np
from PIL import Image, ImageTk


class DicomImageDisplay:
    def __init__(self, canvas, with_window=True, print_window=False):
        self.canvas = canvas
        self.image_id = None
        self.original_image = None
        self.windowed_image = None
        self.window_width = None
        self.window_centre = None
        self.image = None
        self.text_id = None
        self.with_window=with_window
        self.print_window=print_window
        self.prev_coords = None

    def set_default_image(self):
        self.canvas.update()
        array_img = np.ndarray(self.canvas_dimensions())
        color = 255
        array_img.fill(color)
        self.original_image = array_img
        self.image = self._np_array_to_image(array_img)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def set_image(self, image, window_width, window_centre):
        self.canvas.update()
        self.original_image = image
        if self.with_window:
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
        return self.window_width + 2 * dx, self.window_centre + 2 * dy

    def _update_image(self):
        self.windowed_image = self.apply_window(self.original_image)
        self.image = self._np_array_to_image(self.windowed_image)
        self.canvas.itemconfig(self.image_id, image=self.image)
        if self.with_window and self.print_window:
            text = "L: {:.2f}\nW: {:.2f}".format(round(self.window_centre, 2), round(self.window_width), 2)
            color = self._calculate_params_label_text_color()
            if self.text_id is None:
                self.text_id = self.canvas.create_text(*self._calculate_params_label_location(), text=text,
                                                       font=('Consolas', 12), fill=color)
            else:
                self.canvas.itemconfig(self.text_id, text=text, font=('Consolas', 12), fill=color)

    def _calculate_params_label_location(self):
        x, y = self.canvas_dimensions()
        return x - 50, y - 25

    def _calculate_params_label_text_color(self):
        x, y = self.canvas_dimensions()
        xi, yi = self.windowed_image.shape[1], self.windowed_image.shape[0]
        avg = np.mean(self.windowed_image[int(yi - (50.0 * yi / y)):, int(xi - (100.0 * xi / x)):])
        return '#ffffff' if avg < 150 else '#000000'

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
        if not self.with_window:
            return image
        img = np.ndarray(image.shape)
        for i in range(len(image)):
            for j in range(len(image[i])):
                img[i][j] = self._map_pixel(image[i][j], self.window_width, self.window_centre)
        return img

    def canvas_dimensions(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()






