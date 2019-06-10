import os
import tkinter as tk
from tkinter import messagebox
from tkinter.colorchooser import askcolor

import numpy as np
import pydicom
from PIL import Image, ImageTk

from viewer.command.command_executor import CommandExecutor
from viewer.dicom_utils.io import read_dicom
from viewer.drawer import Drawer


class MainWindow:
    VERSION = 1.0
    REPO_LINK = 'https://github.com/Lukasz1928/DICOM-viewer/'

    def __init__(self, main: tk.Tk):
        self.main = main
        self._setup_canvas()
        self._setup_default_bindings()
        self._setup_initial_image()
        self._setup_preview()
        self._setup_menubar()
        self._setup_menu()

        self.dcm = None

    def _setup_default_bindings(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.main.bind("<Control-z>", self.executor.undo)
        self.main.bind("<Control-Shift-Z>", self.executor.redo)

    def _setup_initial_image(self):
        self.dir_path = ''
        self._img = np.ndarray(self._canvas_dimensions())
        self.color = 255
        self._img.fill(self.color)
        self.image = Image.fromarray(self._img).resize(self._canvas_dimensions())
        self.img = ImageTk.PhotoImage(image=self.image, master=self.main)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def _setup_preview(self):
        self.preview_count = 6
        self.offset = 0
        self.preview_frame = tk.Frame(master=self.main, height=64, width=512)
        self.preview_frame.grid(row=1, column=0)
        tk.Button(master=self.preview_frame, text="<", command=self.previous_preview, relief="raised") \
            .grid(row=0, column=0)
        tk.Button(master=self.preview_frame, text=">", command=self.next_preview, relief="raised") \
            .grid(row=0, column=self.preview_count + 1)
        self.previews = [tk.Canvas(self.preview_frame, width=64, height=64) for _ in range(self.preview_count)]
        self._img_previews = [np.ndarray((64, 64)) for _ in range(self.preview_count)]
        for _img in self._img_previews:
            _img.fill(self.color)
        self.image_previews = [Image.fromarray(self._img_previews[i]).resize((64, 64)) for i in
                               range(self.preview_count)]
        self.img_previews = [ImageTk.PhotoImage(image=self.image_previews[i], master=self.main) for i in
                             range(self.preview_count)]
        self.image_on_canvas_previews = []
        self.preview_labels = [tk.Label(self.preview_frame, text='', height=1, width=6) for _ in
                               range(self.preview_count)]
        for i in range(self.preview_count):
            self.preview_labels[i].grid(row=1, column=i + 1)
            self.preview_labels[i].bind("<ButtonRelease-1>",
                                        self.get_load_preview_image(i))
            self.previews[i].bind("<ButtonRelease-1>",
                                  self.get_load_preview_image(i))
            self.previews[i].grid(row=0, column=i + 1)
            self.image_on_canvas_previews.append(self.previews[i].create_image(0, 0, anchor=tk.NW,
                                                                               image=self.img_previews[i]))

    def get_load_preview_image(self, image_number):
        def _load_preview_image(event):
            self._open_image(self.preview_labels[image_number]['text'] + '.dcm')

        return _load_preview_image

    def _setup_menubar(self):
        menubar = tk.Menu(self.main)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Open', command=self._open_file)
        menubar = tk.Menu(self.main)
        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_command(label='Info', command=self._show_info)
        self.main.config(menu=menubar)

    def _setup_canvas(self):
        self.canvas = tk.Canvas(self.main, width=512, height=512)
        self.executor = CommandExecutor(self.canvas, None)
        self.drawer = Drawer(self.canvas, self.executor)
        self.canvas.grid(row=2, column=0)
        self.canvas.update()

    def _setup_drawing_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.drawer.draw_curve)
        self.canvas.bind("<B1-Motion>", self.drawer.draw_curve)
        self.canvas.bind("<ButtonRelease-1>", self.drawer.draw_curve)

    def _setup_angle_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.drawer.draw_angle)
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
            self._reset_drawer()
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
            self._reset_drawer()
            self._setup_angle_bindings()
            self.angle_button.config(relief="sunken")

    def _rectangle_button_command(self):
        if self.rectangle_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.rectangle_button.config(relief="raised")
        else:
            self._reset_drawer()
            self._setup_rectangle_bindings()
            self.rectangle_button.config(relief="sunken")

    def _ellipse_button_command(self):
        if self.ellipse_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.ellipse_button.config(relief="raised")
        else:
            self._reset_drawer()
            self._setup_ellipse_bindings()
            self.ellipse_button.config(relief="sunken")

    def _line_button_command(self):
        if self.line_button.config('relief')[-1] == 'sunken':
            self._setup_default_bindings()
            self.line_button.config(relief="raised")
        else:
            self._reset_drawer()
            self._setup_line_bindings()
            self.line_button.config(relief="sunken")

    def _clear_button_command(self):
        self.executor.reset()

    def _reset_drawer(self):
        self._setup_default_bindings()
        self.drawer.reset()
        self.b.config(relief="raised")
        self.angle_button.config(relief="raised")
        self.rectangle_button.config(relief="raised")
        self.ellipse_button.config(relief="raised")
        self.line_button.config(relief="raised")

    def _setup_menu(self):
        self.button_frame = tk.Frame(self.main)
        self.button_frame.grid(row=2, column=1)
        self.b = tk.Button(self.button_frame, text="Draw", command=self._draw_button_command, relief="raised")
        self.b.pack(fill=tk.X)
        self.color_button = tk.Button(self.button_frame, text="Select color", command=self._color_button_command,
                                      relief="raised")
        self.color_button.pack(fill=tk.X)
        self.angle_button = tk.Button(self.button_frame, text="Measure angle", command=self._angle_button_command,
                                      relief="raised")
        self.angle_button.pack(fill=tk.X)
        self.rectangle_button = tk.Button(self.button_frame, text="Rectangle", command=self._rectangle_button_command,
                                          relief="raised")
        self.rectangle_button.pack(fill=tk.X)
        self.ellipse_button = tk.Button(self.button_frame, text="Ellipse", command=self._ellipse_button_command,
                                        relief="raised")
        self.ellipse_button.pack(fill=tk.X)
        self.line_button = tk.Button(self.button_frame, text="Line", command=self._line_button_command, relief="raised")
        self.line_button.pack(fill=tk.X)
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self._clear_button_command,
                                      relief="raised")
        self.clear_button.pack(fill=tk.X)

    def _open_image(self, name):
        if name != '.dcm':
            path = self.dir_path + name
            self.dcm = pydicom.dcmread(path)
            self._draw_image()

    def _open_file(self):
        self.dcm, path = read_dicom()
        if not path:
            return
        self.dir_path = "/".join(path.split("/")[:-1]) + "/"
        if self.dcm is not None:
            self._draw_image()

    def _draw_image(self):
        raw_image = self.dcm.pixel_array

        dicom_files = self._list_dicoms_from_dir()
        self.load_previews(dicom_files[self.offset:self.offset + self.preview_count])

        self.drawer.pixel_spacing = self.dcm.data_element("PixelSpacing").value

        self.drawer.rescale_factor = (self._canvas_dimensions()[0] / self.dcm.pixel_array.shape[0],
                                      self._canvas_dimensions()[1] / self.dcm.pixel_array.shape[1])
        self.drawer.measure = True

        self.image = Image.fromarray(raw_image).resize(self._canvas_dimensions())
        self.img = ImageTk.PhotoImage(image=self.image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)
        self.executor.undo_all()
        self.executor.clear()

    def _list_dicoms_from_dir(self):
        return list(map(lambda name: self.dir_path + name,
                        filter(lambda file: file.endswith(".dcm"), os.listdir(self.dir_path))))

    def update_window(self, event=None):
        self.image = Image.fromarray(self._img).resize(self._canvas_dimensions())
        self.img = ImageTk.PhotoImage(image=self.image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)

    def _canvas_dimensions(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()

    def previous_preview(self, event=None):
        if not self.dir_path:
            return
        dicom_files = self._list_dicoms_from_dir()
        if self.offset > 0:
            self.offset -= 1
            self.load_previews(dicom_files[self.offset:self.offset + self.preview_count])

    def next_preview(self, event=None):
        if not self.dir_path:
            return
        dicom_files = self._list_dicoms_from_dir()
        if self.offset < len(dicom_files) - self.preview_count:
            self.offset += 1
            self.load_previews(dicom_files[self.offset:self.offset + self.preview_count])

    def load_previews(self, image_paths):
        for index, path in enumerate(image_paths):
            self.load_preview(index, path)
        for index in range(len(image_paths), self.preview_count):
            self.load_preview(index, '')

    def load_preview(self, index, path):
        if path:
            self._img_previews[index] = pydicom.dcmread(path).pixel_array
        else:
            self._img_previews[index].fill(self.color)
        self.image_previews[index] = Image.fromarray(self._img_previews[index]) \
            .resize((self.previews[index].winfo_width(), self.previews[index].winfo_height()))
        self.img_previews[index] = ImageTk.PhotoImage(image=self.image_previews[index])
        self.previews[index].itemconfig(self.image_on_canvas_previews[index], image=self.img_previews[index])
        self.preview_labels[index].config(text=path.split('/')[-1].split('.')[0] if path else '')

    def _show_info(self):
        messagebox.showinfo("DICOM Viewer", "Authors:\nLukasz Niemiec\nMichal Zakrzewski\n\nVersion:{}\n\n{}"
                            .format(self.VERSION, self.REPO_LINK))


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
