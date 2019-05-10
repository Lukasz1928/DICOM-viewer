import pydicom
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2


class MainWindow():

    # ds = pydicom.dcmread("./data/head.dcm")
    # data = ds.pixel_array

    def __init__(self, main):
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


    def transformData(self, data, window, level):
        return data

    def initWindow(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))

    def updateWindow(self, event):
        #print("x: " + str(event.x) + " y: " + str(event.y))
        self._img = np.ndarray([512, 512])
        print(self.color)
        self._img.fill(self.color)
        self.color = (self.color + 10) % 256
        self.image2 = Image.fromarray(self._img)
        self.image2 = self.image2.resize((512, 512), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(image=self.image2)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img2)



def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
