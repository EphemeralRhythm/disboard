class Command:
    def __init__(self, name, author, x=0, y=0, target=None):
        self.name = name
        self.author = author
        self.x = x
        self.y = y
        self.target = target
