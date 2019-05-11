import tkinter as tk
from tkinter import filedialog

import numpy as np
import pydicom
from PIL import Image, ImageTk


class MainWindow():

    # ds = pydicom.dcmread("./data/head.dcm")
    # data = ds.pixel_array

    def __init__(self, main: tk.Tk):
        self.canvas = tk.Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.initWindow)
        self.canvas.bind("<Button-3>", self.updateWindow)
        # self.canvas.bind("<B1-Motion>", self.updateWindow)

        # self.array = self.data
        # self.image = Image.fromarray(self.array)
        # self.image = self.image.resize((512, 512), Image.ANTIALIAS)
        self._img = np.ndarray([512, 512])
        self.color = 0
        print('dupa')
        self._img.fill(self.color)
        self.image = Image.fromarray(self._img)
        self.image = self.image.resize((512, 512), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image=self.image, master=main)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        menubar = tk.Menu(main)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        menubar = tk.Menu(main)
        menubar.add_cascade(label="File", menu=filemenu)

        main.config(menu=menubar)

    def transform_data(self, data, window, level):
        return data

    def init_window(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))

    def open_file(self):
        path = filedialog.askopenfilename(initialdir=".", title="Select file",
                                          filetypes=(("DICOM files", "*.dcm"),))
        if path != '':
            self._img = pydicom.dcmread(path).pixel_array
            self.updateWindow()

    def update_window(self, event=None):
        # print("x: " + str(event.x) + " y: " + str(event.y))
        # self._img = np.ndarray([512, 512])
        # print(self.color)
        # self._img.fill(self.color)
        # self.color = (self.color + 10) % 256
        image2 = Image.fromarray(self._img)
        image2 = image2.resize((512, 512), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(image=image2)
        self.canvas.itemconfig(self.image_on_canvas, image=img2)


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
