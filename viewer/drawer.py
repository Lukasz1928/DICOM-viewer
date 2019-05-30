from viewer.command.command import LineCommand, ComplexCommand, AngleCommand, RectangleCommand, EllipseCommand, \
    DistanceCommand


class Drawer:
    def __init__(self, canvas, executor, pixel_spacing=None):
        self.canvas = canvas
        self.executor = executor
        self.prev_points = None
        self.color = 'red'
        self.pixel_spacing = pixel_spacing
        self.draw_command = None

    def draw_curve(self, event):
        x, y = event.x, event.y
        if self.prev_points is not None:
            dc = LineCommand(self.canvas, (x, y), self.prev_points, color=self.color)
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

    def draw_rectangle(self, event):
        x, y = event.x, event.y
        r = False
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = RectangleCommand(self.canvas, self.color, self.pixel_spacing)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
                self.executor.add(self.draw_command)
        if r:
            self.draw_command = None

    def draw_ellipse(self, event):
        x, y = event.x, event.y
        r = False
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = EllipseCommand(self.canvas, self.color, self.pixel_spacing)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
                self.executor.add(self.draw_command)
        if r:
            self.draw_command = None

    def draw_line(self, event):
        x, y = event.x, event.y
        r = False
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = DistanceCommand(self.canvas, self.color, self.pixel_spacing)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
                self.executor.add(self.draw_command)
        if r:
            self.draw_command = None

    def set_color(self, color):
        self.color = color
