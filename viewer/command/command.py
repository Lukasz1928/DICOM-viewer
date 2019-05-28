from abc import ABC


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
