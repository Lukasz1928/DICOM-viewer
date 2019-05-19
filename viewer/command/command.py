from abc import ABC


class Command(ABC):
    def execute(self, canvas):
        pass


class ComplexCommand(Command):
    def __init__(self, commands):
        self.commands = commands

    def execute(self, canvas):
        for c in self.commands:
            c.execute(canvas)





class DrawCommand: