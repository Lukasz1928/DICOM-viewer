from viewer.command.command import DrawLineCommand, ComplexCommand


class Drawer:
    def __init__(self, canvas, executor):
        self.canvas = canvas
        self.executor = executor
        self.prev_curve_point = None
        self.color = 'red'
        self.draw_curve_command = None

    def draw_curve(self, event):
        x, y = event.x, event.y
        if self.prev_curve_point is not None:
            dc = DrawLineCommand(self.canvas, (x, y), self.prev_curve_point, color=self.color)
            self.draw_curve_command.add_command(dc)
        else:
            self.draw_curve_command = ComplexCommand(self.canvas)
        self.prev_curve_point = (x, y)

    def reset_curve(self, event):
        self.prev_curve_point = None
        self.executor.add(self.draw_curve_command)
        self.draw_curve_command = None
        print(self.executor.done)

    def set_color(self, color):
        self.color = color
