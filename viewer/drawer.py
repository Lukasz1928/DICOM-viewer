from viewer.command.command import LineCommand, ComplexCommand, AngleCommand, RectangleCommand, EllipseCommand, \
    DistanceCommand, CurveCommand
from viewer.command.status import CommandStatus


class Drawer:
    def __init__(self, canvas, executor, pixel_spacing=None, rescale_factor=None):
        self.canvas = canvas
        self.executor = executor
        self.color = 'red'
        self.pixel_spacing = pixel_spacing if pixel_spacing is not None else [1, 1]
        self.rescale_factor = rescale_factor if rescale_factor is not None else [1, 1]
        self.measure = False
        self.draw_command = None

    def draw_curve(self, event):
        x, y = event.x, event.y
        r = None
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = CurveCommand(self.canvas, self.color)
                r = self.draw_command.add_point((x, y))
        if r == CommandStatus.SUCCESS:
            self.executor.add(self.draw_command)
            self.reset()
        elif r == CommandStatus.FAIL:
            self.draw_command.undo()
            self.reset()

    def reset(self):
        self.draw_command = None

    def draw_angle(self, event):
        x, y = event.x, event.y
        r = None
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '4' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = AngleCommand(self.canvas, self.color, self.pixel_spacing, self.rescale_factor,
                                                 with_measurement=self.measure)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
        if r == CommandStatus.SUCCESS:
            self.executor.add(self.draw_command)
            self.reset()
        elif r == CommandStatus.FAIL:
            self.draw_command.undo()
            self.reset()

    def draw_rectangle(self, event):
        x, y = event.x, event.y
        r = None
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = RectangleCommand(self.canvas, self.color, self.pixel_spacing, self.rescale_factor,
                                                     with_measurement=self.measure)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
        if r == CommandStatus.SUCCESS:
            self.executor.add(self.draw_command)
            self.reset()
        elif r == CommandStatus.FAIL:
            self.draw_command.undo()
            self.reset()

    def draw_ellipse(self, event):
        x, y = event.x, event.y
        r = None
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = EllipseCommand(self.canvas, self.color, self.pixel_spacing, self.rescale_factor,
                                                   with_measurement=self.measure)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
        if r == CommandStatus.SUCCESS:
            self.executor.add(self.draw_command)
            self.reset()
        elif r == CommandStatus.FAIL:
            self.draw_command.undo()
            self.reset()

    def draw_line(self, event):
        x, y = event.x, event.y
        r = None
        if self.draw_command is not None:
            r = self.draw_command.add_point((x, y), final=event.type == '5' and event.num == 1)
        else:
            if event.type == '4' and event.num == 1:
                self.draw_command = DistanceCommand(self.canvas, self.color, self.pixel_spacing, self.rescale_factor,
                                                    with_measurement=self.measure)
                _ = self.draw_command.add_point((x, y), final=True)
                r = self.draw_command.add_point((x, y))
        if r == CommandStatus.SUCCESS:
            self.executor.add(self.draw_command)
            self.reset()
        elif r == CommandStatus.FAIL:
            self.draw_command.undo()
            self.reset()

    def set_color(self, color):
        self.color = color
