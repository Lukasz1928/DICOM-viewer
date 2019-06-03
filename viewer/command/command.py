import math
from abc import ABC
import numpy as np


class Command(ABC):
    def execute(self):
        pass

    def undo(self):
        pass


class ComplexCommand(Command):
    def __init__(self, canvas, commands=None):
        self.canvas = canvas
        if commands is None:
            commands = []
        self.commands = commands

    def execute(self):
        for c in self.commands:
            c.execute()

    def add_command(self, command, execute=True):
        self.commands.append(command)
        if execute:
            command.execute()

    def undo(self):
        for c in reversed(self.commands):
            c.undo()


class CurveCommand(ComplexCommand):
    def __init__(self, canvas, color):
        ComplexCommand.__init__(self, canvas)
        self.color = color
        self.prev_point = None

    def add_point(self, point, final=False):
        if self.prev_point is not None:
            dc = LineCommand(self.canvas, self.prev_point, point, self.color)
            dc.execute()
            self.commands.append(dc)
        self.prev_point = point
        return final


class TextCommand(Command):
    def __init__(self, canvas, text, color, location):
        self.id = None
        self.canvas = canvas
        self.text = text
        self.color = color
        self.location = location

    def execute(self):
        self.id = self.canvas.create_text(self.location[0], self.location[1], text=self.text, fill=self.color)

    def undo(self):
        self.canvas.delete(self.id)


class LineCommand(Command):
    def __init__(self, canvas, start_point, end_point, color):
        self.id = None
        self.start_point = start_point
        self.end_point = end_point
        self.canvas = canvas
        self.color = color

    def execute(self):
        self.id = self.canvas.create_line(self.start_point[0], self.start_point[1],
                                          self.end_point[0], self.end_point[1], fill=self.color, width=3)

    def undo(self):
        self.canvas.delete(self.id)


class AngleCommand(ComplexCommand):
    def __init__(self, canvas, color, pixel_spacing, rescale_factor, with_measurement=True):
        ComplexCommand.__init__(self, canvas)
        self.color = color
        self.points = []
        self.confirmed = 0
        self.pixel_spacing = pixel_spacing
        self.rescale_factor = rescale_factor
        self.measure = with_measurement

    def add_point(self, point, final=False):
        if final:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            self.confirmed += 1
            if len(self.points) in [2, 3]:
                command = LineCommand(self.canvas, self.points[len(self.points) - 2],
                                      self.points[len(self.points) - 1], self.color)
                command.execute()
                self.commands.append(command)
        else:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            if len(self.points) in [2, 3]:
                command = LineCommand(self.canvas, self.points[len(self.points) - 2],
                                      self.points[len(self.points) - 1], self.color)
                command.execute()
                self.commands.append(command)

        finished = final and len(self.points) == 3
        if finished and self.measure:
            angle = self._calculate_angle()
            self._print_angle_label(angle)
        return finished

    def _calculate_angle(self):
        p1, p2, p3 = self.points[0], self.points[1], self.points[2]
        v1 = ((p1[0] - p2[0]) * self.pixel_spacing[0] / self.rescale_factor[0],
              (p1[1] - p2[1]) * self.pixel_spacing[1] / self.rescale_factor[1])
        v2 = ((p3[0] - p2[0]) * self.pixel_spacing[0] / self.rescale_factor[0],
              (p3[1] - p2[1]) * self.pixel_spacing[1] / self.rescale_factor[1])
        angle = math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        deg_angle = round(180 / math.pi * angle, 2)
        return deg_angle

    def _print_angle_label(self, angle):
        loc = self._calculate_label_location()
        text_command = TextCommand(self.canvas, angle, self.color, loc)
        text_command.execute()
        self.commands.append(text_command)

    def _calculate_label_location(self):
        distance = 10
        v1 = (self.points[1][0] - self.points[0][0], self.points[1][1] - self.points[0][1])
        v2 = (self.points[1][0] - self.points[2][0], self.points[1][1] - self.points[2][1])
        norm_v1 = [x / np.linalg.norm(v1) for x in v1]
        norm_v2 = [x / np.linalg.norm(v2) for x in v2]
        label_vector = (norm_v1[0] + norm_v2[0], norm_v1[1] + norm_v2[1])
        norm_label_vector = [x / np.linalg.norm(label_vector) for x in label_vector]
        dx = distance * norm_label_vector[0]
        dy = distance * norm_label_vector[1]
        loc = (self.points[1][0] + dx, self.points[1][1] + dy)
        return loc


class RectangleCommand(ComplexCommand):
    def __init__(self, canvas, color, pixel_spacing, rescale_factor, with_measurement=True):
        ComplexCommand.__init__(self, canvas)
        self.color = color
        self.points = []
        self.confirmed = 0
        self.pixel_spacing = pixel_spacing
        self.rescale_factor = rescale_factor
        self.measure = with_measurement

    class RectCommand(Command):
        def __init__(self, canvas, point1, point2, color):
            self.canvas = canvas
            self.color = color
            self.point1 = point1
            self.point2 = point2
            self.id = None

        def execute(self):
            self.id = self.canvas.create_rectangle(self.point1[0], self.point1[1], self.point2[0], self.point2[1],
                                                   outline=self.color, width=3)

        def undo(self):
            self.canvas.delete(self.id)

    def add_point(self, point, final=False):
        if final:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            self.confirmed += 1
            if len(self.points) == 2:
                command = self.RectCommand(self.canvas, self.points[0], self.points[1], self.color)
                command.execute()
                self.commands.append(command)
        else:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            if len(self.points) == 2:
                command = self.RectCommand(self.canvas, self.points[0], self.points[1], self.color)
                command.execute()
                self.commands.append(command)
        finished = final and len(self.points) == 2
        if finished and self.measure:
            self._print_label()
        return finished

    def _calculate_label_location(self):
        dx = 0
        dy = 20
        x, y = max([x[0] for x in self.points]) + dx, max([x[1] for x in self.points]) + dy
        if x >= self.canvas.winfo_width():
            x = x - 2 * dx
        if y >= self.canvas.winfo_width():
            y = y - 2 * dy
        return x, y

    def _print_label(self):
        loc = self._calculate_label_location()
        area = round(self._calculate_area(), 2)
        perimeter = round(self._calculate_perimeter(), 2)
        text = "Area: {} mm2\nPerim.: {} mm".format(area, perimeter)
        text_command = TextCommand(self.canvas, text, self.color, loc)
        text_command.execute()
        self.commands.append(text_command)

    def _calculate_area(self):
        width = abs(self.points[0][0] - self.points[1][0]) * self.pixel_spacing[0] / self.rescale_factor[0]
        height = abs(self.points[0][1] - self.points[1][1]) * self.pixel_spacing[1] / self.rescale_factor[1]
        return width * height

    def _calculate_perimeter(self):
        width = abs(self.points[0][0] - self.points[1][0]) * self.pixel_spacing[0] / self.rescale_factor[0]
        height = abs(self.points[0][1] - self.points[1][1]) * self.pixel_spacing[1] / self.rescale_factor[1]
        return 2 * (width + height)


class EllipseCommand(ComplexCommand):
    def __init__(self, canvas, color, pixel_spacing, rescale_factor, with_measurement=True):
        ComplexCommand.__init__(self, canvas)
        self.color = color
        self.points = []
        self.confirmed = 0
        self.pixel_spacing = pixel_spacing
        self.rescale_factor = rescale_factor
        self.measure = with_measurement

    class OvalCommand(Command):
        def __init__(self, canvas, point1, point2, color):
            self.canvas = canvas
            self.color = color
            self.point1 = point1
            self.point2 = point2
            self.id = None

        def execute(self):
            self.id = self.canvas.create_oval(self.point1[0], self.point1[1], self.point2[0], self.point2[1],
                                              outline=self.color, width=3)

        def undo(self):
            self.canvas.delete(self.id)

    def add_point(self, point, final=False):
        if final:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            self.confirmed += 1
            if len(self.points) == 2:
                command = self.OvalCommand(self.canvas, self.points[0], self.points[1], self.color)
                command.execute()
                self.commands.append(command)
        else:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            if len(self.points) == 2:
                command = self.OvalCommand(self.canvas, self.points[0], self.points[1], self.color)
                command.execute()
                self.commands.append(command)
        finished = final and len(self.points) == 2
        if finished and self.measure:
            self._print_label()
        return finished

    def _calculate_label_location(self):
        dx = 0
        dy = 20
        x, y = max([x[0] for x in self.points]) + dx, max([x[1] for x in self.points]) + dy
        if x >= self.canvas.winfo_width():
            x = x - 2 * dx
        if y >= self.canvas.winfo_width():
            y = y - 2 * dy
        return x, y

    def _print_label(self):
        loc = self._calculate_label_location()
        area = round(self._calculate_area(), 2)
        perimeter = round(self._calculate_perimeter(), 2)
        text = "Area: {} mm2\nPerim.: {} mm".format(area, perimeter)
        text_command = TextCommand(self.canvas, text, self.color, loc)
        text_command.execute()
        self.commands.append(text_command)

    def _calculate_area(self):
        width = abs(self.points[0][0] - self.points[1][0]) / 2.0 * self.pixel_spacing[0] / self.rescale_factor[0]
        height = abs(self.points[0][1] - self.points[1][1]) / 2.0 * self.pixel_spacing[1] / self.rescale_factor[1]
        return width * height * math.pi

    def _calculate_perimeter(self):
        width = abs(self.points[0][0] - self.points[1][0]) / 2.0 * self.pixel_spacing[0] / self.rescale_factor[0]
        height = abs(self.points[0][1] - self.points[1][1]) / 2.0 * self.pixel_spacing[1] / self.rescale_factor[1]
        h = ((width - height) ** 2) / ((width + height) ** 2)
        return math.pi * (width + height) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))


class DistanceCommand(ComplexCommand):
    def __init__(self, canvas, color, pixel_spacing, rescale_factor, with_measurement=True):
        ComplexCommand.__init__(self, canvas)
        self.color = color
        self.points = []
        self.confirmed = 0
        self.pixel_spacing = pixel_spacing
        self.rescale_factor = rescale_factor
        self.measure = with_measurement

    def add_point(self, point, final=False):
        if final:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            self.confirmed += 1
            if len(self.points) == 2:
                command = LineCommand(self.canvas, self.points[0], self.points[1], self.color)
                command.execute()
                self.commands.append(command)
        else:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            if len(self.points) == 2:
                command = LineCommand(self.canvas, self.points[0], self.points[1], self.color)
                command.execute()
                self.commands.append(command)
        finished = final and len(self.points) == 2
        if finished and self.measure:
            self._print_label()
        return finished

    def _calculate_label_location(self):
        x_r, y_r = max(self.points, key=lambda p: p[0])
        x_l, y_l = min(self.points, key=lambda p: p[0])
        if x_l == x_r or (y_r - y_l) / (x_r - x_l) < -0.5:
            dx = 45
            dy = 10
        elif (y_r - y_l) / (x_r - x_l) > 0:
            dx = 0
            dy = 10
        else:
            dx = 0
            dy = -10
        return x_r + dx, y_r + dy

    def _print_label(self):
        loc = self._calculate_label_location()
        length = round(self._calculate_length(), 2)
        text = "Length: {} mm".format(length)
        text_command = TextCommand(self.canvas, text, self.color, loc)
        text_command.execute()
        self.commands.append(text_command)

    def _calculate_length(self):
        dx = (self.points[0][0] - self.points[1][0]) * self.pixel_spacing[0] / self.rescale_factor[0]
        dy = (self.points[0][1] - self.points[1][1]) * self.pixel_spacing[1] / self.rescale_factor[1]
        return math.sqrt(dx ** 2 + dy ** 2)
