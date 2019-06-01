import tkinter as tk
from tkinter.colorchooser import askcolor

import numpy as np
from PIL import Image, ImageTk

from viewer.command.command_executor import CommandExecutor
from viewer.dicom_utils.io import read_dicom
from viewer.drawer import Drawer


class MainWindow:

    def __init__(self, main: tk.Tk):
        self.main = main
        self._setup_canvas()
        self._setup_default_bindings()
        self._setup_initial_image()
        self._setup_menubar()
        self._setup_menu()

        self.dcm = None

    def _setup_default_bindings(self):
        self.main.bind("<Control-z>", self.executor.undo)
        self.main.bind("<Control-Shift-Z>", self.executor.redo)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def _setup_initial_image(self):
        self._img = np.ndarray(self._canvas_dimensions())
        self.color = 255
        self._img.fill(self.color)
        self.image = Image.fromarray(self._img).resize(self._canvas_dimensions())
        self.img = ImageTk.PhotoImage(image=self.image, master=self.main)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def _setup_menubar(self):
        menubar = tk.Menu(self.main)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self._open_file)
        menubar = tk.Menu(self.main)
        menubar.add_cascade(label="File", menu=filemenu)
        self.main.config(menu=menubar)

    def _setup_canvas(self):
        self.canvas = tk.Canvas(self.main, width=512, height=512)
        self.executor = CommandExecutor(self.canvas, None)
        self.drawer = Drawer(self.canvas, self.executor)
        self.canvas.grid(row=1, column=0)
        self.canvas.update()

    def _setup_drawing_bindings(self):
        self.canvas.bind("<B1-Motion>", self.drawer.draw_curve)
        self.canvas.bind("<ButtonRelease-1>", self.drawer.reset_curve)

    def _setup_angle_bindings(self):
        self.canvas.bind("<Button-1>", self.drawer.draw_angle)
        self.canvas.bind("<Motion>", self.drawer.draw_angle)

    def _setup_rectangle_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.drawer.draw_rectangle)
        self.canvas.bind("<Motion>", self.drawer.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.drawer.draw_rectangle)

    def _setup_ellipse_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.drawer.draw_ellipse)
        self.canvas.bind("<Motion>", self.drawer.draw_ellipse)
        self.canvas.bind("<ButtonRelease-1>", self.drawer.draw_ellipse)

    def _setup_line_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.drawer.draw_line)
        self.canvas.bind("<Motion>", self.drawer.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.drawer.draw_line)

    def _draw_button_command(self):
        if self.b.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.b.config(relief="raised")
        else:
            self._setup_drawing_bindings()
            self.b.config(relief="sunken")

    def _color_button_command(self):
        color = askcolor()
        self.drawer.set_color(color[1])

    def _angle_button_command(self):
        if self.angle_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.angle_button.config(relief="raised")
        else:
            self._setup_angle_bindings()
            self.angle_button.config(relief="sunken")

    def _rectangle_button_command(self):
        if self.rectangle_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.rectangle_button.config(relief="raised")
        else:
            self._setup_rectangle_bindings()
            self.rectangle_button.config(relief="sunken")

    def _ellipse_button_command(self):
        if self.ellipse_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.ellipse_button.config(relief="raised")
        else:
            self._setup_ellipse_bindings()
            self.ellipse_button.config(relief="sunken")

    def _line_button_command(self):
        if self.line_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.line_button.config(relief="raised")
        else:
            self._setup_line_bindings()
            self.line_button.config(relief="sunken")

    def _setup_menu(self):
        self.b = tk.Button(self.main, text="Draw", command=self._draw_button_command, relief="raised")
        self.b.grid(row=0, column=0)
        self.color_button = tk.Button(self.main, text="Select color", command=self._color_button_command, relief="raised")
        self.color_button.grid(row=0, column=1)
        self.angle_button = tk.Button(self.main, text="Measure angle", command=self._angle_button_command, relief="raised")
        self.angle_button.grid(row=0, column=2)
        self.rectangle_button = tk.Button(self.main, text="Rectangle", command=self._rectangle_button_command, relief="raised")
        self.rectangle_button.grid(row=0, column=3)
        self.ellipse_button = tk.Button(self.main, text="Ellipse", command=self._ellipse_button_command, relief="raised")
        self.ellipse_button.grid(row=0, column=4)
        self.line_button = tk.Button(self.main, text="Line", command=self._line_button_command, relief="raised")
        self.line_button.grid(row=0, column=5)

    def _open_file(self):
        self.dcm = read_dicom()
        if self.dcm is not None:
            raw_image = self.dcm.pixel_array

            self.drawer.pixel_spacing = self.dcm.data_element("PixelSpacing").value
            print(self.dcm.data_element("PixelSpacing").value)
            self.drawer.rescale_factor = (self._canvas_dimensions()[0] / self.dcm.pixel_array.shape[0],
                                          self._canvas_dimensions()[1] / self.dcm.pixel_array.shape[1])

            self.image = Image.fromarray(raw_image).resize(self._canvas_dimensions())
            self.img = ImageTk.PhotoImage(image=self.image)
            self.canvas.itemconfig(self.image_on_canvas, image=self.img)
            self.executor.undo_all()
            self.executor.clear()

    def _canvas_dimensions(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
