from viewer.command.command import DrawLineCommand, ComplexCommand, AngleCommand


class Drawer:
    def __init__(self, canvas, executor):
        self.canvas = canvas
        self.executor = executor
        self.prev_points = None
        self.color = 'red'
        self.draw_command = None

    def draw_curve(self, event):
        x, y = event.x, event.y
        if self.prev_points is not None:
            dc = DrawLineCommand(self.canvas, (x, y), self.prev_points, color=self.color)
            self.draw_command.add_command(dc)
        else:
            self.draw_command = ComplexCommand(self.canvas)
        self.prev_points = (x, y)

    def reset_curve(self, event):
        self.prev_points = None
        self.executor.add(self.draw_command)
        self.draw_command = None

    def draw_angle(self, event):
        x, y = event.x, event.y
        r = False
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '4' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = AngleCommand(self.canvas, self.color)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
                self.executor.add(self.draw_command)
        if r:
            self.draw_command = None


    def set_color(self, color):
        self.color = color
