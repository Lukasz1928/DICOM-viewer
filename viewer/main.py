import os
import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor

import numpy as np
import pydicom
from PIL import Image, ImageTk

from viewer.command.command_executor import CommandExecutor
from viewer.drawer import Drawer


class MainWindow:

    def __init__(self, main: tk.Tk):
        self.main = main
        self.setup_preview()
        self.setup_canvas()
        self.setup_default_bindings()
        self.setup_initial_image()
        self.setup_menubar()
        self.setup_menu()

    def setup_default_bindings(self):
        self.main.bind("<Control-z>", self.executor.undo)
        self.main.bind("<Control-Shift-Z>", self.executor.redo)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def setup_initial_image(self):
        self.dir_path = ''
        self._img = np.ndarray(self._canvas_dimensions())
        self.color = 255
        self._img.fill(self.color)
        self.image = Image.fromarray(self._img).resize(self._canvas_dimensions())
        self.img = ImageTk.PhotoImage(image=self.image, master=self.main)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def setup_preview(self):
        self.preview_count = 6
        self.offset = 0
        self.preview_frame = tk.Frame(master=self.main, height=64, width=512)
        self.preview_frame.grid(row=1, column=0)
        for i in range(0, self.preview_count):
            tk.Label(master=self.preview_frame, text=str(i)).grid(row=0, column=i + 1)
        tk.Button(master=self.preview_frame, text="<", command=self.previous_preview, relief="raised") \
            .grid(row=0, column=0)
        tk.Button(master=self.preview_frame, text=">", command=self.next_preview, relief="raised") \
            .grid(row=0, column=self.preview_count + 1)
        self.previews = [tk.Canvas(self.preview_frame, width=64, height=64) for _ in range(0, self.preview_count)]
        self._img_previews = [np.ndarray((64, 64)) for _ in range(0, self.preview_count)]
        self.image_previews = [Image.fromarray(self._img_previews[i]).resize((64, 64)) for i in
                               range(0, self.preview_count)]
        self.img_previews = [ImageTk.PhotoImage(image=self.image_previews[i], master=self.main) for i in
                             range(0, self.preview_count)]
        self.image_on_canvas_previews = []
        self.preview_labels = [tk.Label(self.preview_frame, text='a', height=1, width=6) for _ in range(0, self.preview_count)]
        for i in range(0, self.preview_count):
            self.preview_labels[i].grid(row=1, column=i + 1)
            # self.preview_labels[i].bind("<ButtonRelease-1>",
            #                             lambda event: self.mock(event, self.preview_labels[i]['text']))
            self.previews[i].grid(row=0, column=i + 1)
            self.image_on_canvas_previews.append(self.previews[i].create_image(0, 0, anchor=tk.NW,
                                                                               image=self.img_previews[i]))

    def _mock_event(self, event, *args):
        print(event)
        print(args)

    def setup_menubar(self):
        menubar = tk.Menu(self.main)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        menubar = tk.Menu(self.main)
        menubar.add_cascade(label="File", menu=filemenu)
        self.main.config(menu=menubar)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.main, width=512, height=512)
        self.executor = CommandExecutor(self.canvas, None)
        self.drawer = Drawer(self.canvas, self.executor)
        self.canvas.grid(row=2, column=0)
        self.canvas.update()

    def setup_drawing_bindings(self):
        self.canvas.bind("<B1-Motion>", self.drawer.draw_curve)
        self.canvas.bind("<ButtonRelease-1>", self.drawer.reset_curve)

    def draw_button_command(self):
        if self.b.config('relief')[-1] == 'sunken':
            self.setup_default_bindings()
            self.b.config(relief="raised")
        else:
            self.setup_drawing_bindings()
            self.b.config(relief="sunken")

    def color_button_command(self):
        color = askcolor()
        self.drawer.set_color(color[1])

    def setup_menu(self):
        self.b = tk.Button(self.main, text="Draw", command=self.draw_button_command, relief="raised")
        self.b.grid(row=0, column=0)
        self.color_button = tk.Button(self.main, text="Select color", command=self.color_button_command,
                                      relief="raised")
        self.color_button.grid(row=0, column=1)

    def open_file(self):
        self.offset = 0
        path = filedialog.askopenfilename(initialdir=".", title="Select file",
                                          filetypes=(("DICOM files", "*.dcm"),))
        if path != '':
            self.dir_path = "/".join(path.split("/")[:-1]) + "/"
            self._img = pydicom.dcmread(path).pixel_array
            dicom_files = self._list_dicoms_from_dir()
            self.load_previews(dicom_files[self.offset:self.offset + self.preview_count])
            self.update_window()
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
        if self.offset < len(dicom_files):
            self.offset += 1
            self.load_previews(dicom_files[self.offset:self.offset + self.preview_count])

    def load_previews(self, image_paths):
        for index, path in enumerate(image_paths):
            self.load_preview(index, path)

    def load_preview(self, index, path):
        self._img_previews[index] = pydicom.dcmread(path).pixel_array
        self.image_previews[index] = Image.fromarray(self._img_previews[index]) \
            .resize((self.previews[index].winfo_width(), self.previews[index].winfo_height()))
        self.img_previews[index] = ImageTk.PhotoImage(image=self.image_previews[index])
        self.previews[index].itemconfig(self.image_on_canvas_previews[index], image=self.img_previews[index])
        self.preview_labels[index].config(text=path.split('/')[-1].split('.')[0])


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
