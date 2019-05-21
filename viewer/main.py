import tkinter as tk
from tkinter import filedialog

import numpy as np
import pydicom
from PIL import Image, ImageTk

from viewer.drawer import Drawer


class MainWindow:

    def __init__(self, main: tk.Tk):
        self.main = main
        self.canvas = tk.Canvas(main, width=512, height=512)
        self.drawer = Drawer(self.canvas)
        self.canvas.grid(row=1, column=0)

        self.setup_default_bindings()
        self.setup_initial_image()
        self.setup_menubar()
        self.setup_menu()

    def setup_default_bindings(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def setup_initial_image(self):
        self._img = np.ndarray([512, 512])
        self.color = 255
        self._img.fill(self.color)
        self.image = Image.fromarray(self._img).resize((512, 512))
        self.img = ImageTk.PhotoImage(image=self.image, master=self.main)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def setup_menubar(self):
        menubar = tk.Menu(self.main)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        menubar = tk.Menu(self.main)
        menubar.add_cascade(label="File", menu=filemenu)
        self.main.config(menu=menubar)

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

    def setup_menu(self):
        self.b = tk.Button(self.main, text="Draw", command=self.draw_button_command, relief="raised")
        self.b.grid(row=0, column=0)

    def open_file(self):
        path = filedialog.askopenfilename(initialdir=".", title="Select file",
                                          filetypes=(("DICOM files", "*.dcm"),))
        if path != '':
            self._img = pydicom.dcmread(path).pixel_array
            self.update_window()

    def update_window(self, event=None):
        self.image = Image.fromarray(self._img).resize((512, 512))
        self.img = ImageTk.PhotoImage(image=self.image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
