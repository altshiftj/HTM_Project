from Wall import *


class Box:

    # default constructor
    def __init__(self, size):

        n1, n2 = size
        self.width = n1
        self.length = n2

        self.walls = []
        self.walls.append(Wall((0, 0), (n1, 0)))
        self.walls.append(Wall((0, 0), (0, n2)))
        self.walls.append(Wall((n1, 0), (n1, n2)))
        self.walls.append(Wall((0, n2), (n1, n2)))

    def add_object(self, x1,y1, x2,y2):
        self.walls.append(Wall((x1, y1), (x2, y1)))
        self.walls.append(Wall((x1, y1), (x1, y2)))
        self.walls.append(Wall((x2, y1), (x2, y2)))
        self.walls.append(Wall((x1, y2), (x1, y2)))

    def draw(self):
        pass
