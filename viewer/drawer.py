

class Drawer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.prev_curve_point = None
        self.color = 'red'

    def draw_curve(self, event):
        x, y = event.x, event.y
        if self.prev_curve_point is not None:
            _x, _y = self.prev_curve_point
            self.canvas.create_line(x, y, _x, _y, fill=self.color, width=3)
        self.prev_curve_point = (x, y)

    def reset_curve(self, event):
        self.prev_curve_point = None

    def set_color(self, color):  # TODO: add call in main
        self.color = color
