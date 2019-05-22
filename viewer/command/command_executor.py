

class CommandExecutor:
    def __init__(self, canvas, default_image):
        self.done = []
        self.undone = []

        self.canvas = canvas
        self.default_image = default_image

    def execute(self, command):
        command.execute()
        self.add(command)

    def add(self, command):
        self.done.append(command)
        self.undone.clear()

    def undo(self, event=None):
        try:
            command = self.done.pop()
        except IndexError:
            pass  # nothing to be undone - ignore command
        else:
            command.undo()
            self.undone.append(command)

    def redo(self, event=None):
        try:
            command = self.undone.pop()
        except IndexError:
            pass  # nothing to be redone - ignore command
        else:
            command.execute()
            self.done.append(command)

    def undo_all(self):
        while len(self.done) > 0:
            self.undo()

    def clear(self):
        self.done.clear()
        self.undone.clear()
