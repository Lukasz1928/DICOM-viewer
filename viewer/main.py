import pydicom
import tkinter as tk
from PIL import Image, ImageTk


class MainWindow():

    ds = pydicom.dcmread("./data/head.dcm")
    data = ds.pixel_array

    def __init__(self, main):
        self.canvas = tk.Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.initWindow)
        self.canvas.bind("<B1-Motion>", self.updateWindow)
        self.canvas.bind("<Button-3>", self.initMeasure)
        self.canvas.bind("<B3-Motion>", self.updateMeasure)
        self.canvas.bind("<ButtonRelease-3>", self.finishMeasure)

        self.array = self.data
        self.image = Image.fromarray(self.array)
        self.image = self.image.resize((512, 512), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image=self.image, master=main)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def transformData(self, data, window, level):
        return data

    def initWindow(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))

    def updateWindow(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))


    def initMeasure(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))

    def updateMeasure(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))

    def finishMeasure(self, event):
        print("x: " + str(event.x) + " y: " + str(event.y))


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
