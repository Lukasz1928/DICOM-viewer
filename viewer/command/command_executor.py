

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
        print('command added: {}'.format(self.done))

    def undo(self, event):
        print('undo')
        try:
            command = self.done.pop()
        except IndexError:
            pass  # nothing to be undone - ignore command
        else:
            print('undone: {}'.format(command))
            command.undo()
            self.undone.append(command)

    def redo(self, event):
        try:
            command = self.undone.pop()
        except IndexError:
            pass  # nothing to be redone - ignore command
        else:
            command.execute()
            self.done.append(command)
