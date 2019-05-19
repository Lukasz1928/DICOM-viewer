

class CommandExecutor:
    def __init__(self, canvas, default_image):
        self.done = []
        self.undone = []

        self.canvas = canvas
        self.default_image = default_image

    def execute(self, command):
        command.execute()
        self.done.append(command)

    def undo(self):
        command = self.done.pop()
        self.undone.append(command)