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


class DrawLineCommand(Command):
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
    def __init__(self, canvas, color):
        ComplexCommand.__init__(self, canvas)
        self.color = color
        self.points = []
        self.confirmed = 0

    def execute(self):
        super(AngleCommand, self).execute()

    def add_point(self, point, final=False):
        if final:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            self.confirmed += 1
            if len(self.points) in [2, 3]:
                command = DrawLineCommand(self.canvas, self.points[len(self.points) - 2],
                                          self.points[len(self.points) - 1], self.color)
                command.execute()
                self.commands.append(command)
        else:
            if len(self.points) > self.confirmed:
                self.points.pop()
                self.commands.pop().undo()
            self.points.append(point)
            if len(self.points) in [2, 3]:
                command = DrawLineCommand(self.canvas, self.points[len(self.points) - 2],
                                          self.points[len(self.points) - 1], self.color)
                command.execute()
                self.commands.append(command)

        finished = final and len(self.points) == 3
        if finished:
            angle = self._calculate_angle()
            self._print_angle_label(angle)
            return True
        return False

    def undo(self):
        super(AngleCommand, self).undo()
        self.points.clear()

    def _calculate_angle(self):
        p1, p2, p3 = self.points[0], self.points[1], self.points[2]
        v1 = (p1[0] - p2[0], p1[1] - p2[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])
        angle = math.acos((v1[0] * v2[0] + v1[1] * v2[1])/(np.linalg.norm(v1) * np.linalg.norm(v2)))
        deg_angle = round(180 / math.pi * angle, 2)
        return deg_angle

    def _print_angle_label(self, angle):
        loc = self._calculate_label_location()
        text_command = TextCommand(self.canvas, angle, self.color, loc)
        text_command.execute()
        self.commands.append(text_command)

    def _calculate_label_location(self, distance=10):
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
