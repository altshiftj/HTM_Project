from Brain import *
from Eye import *


class Animal:

    def __init__(self, x, y, size, head_direction, field_of_view):
        self.x = x
        self.y = y
        self.size = size
        self.head_direction = head_direction
        self.field_of_view = field_of_view
        self.brain = Brain()
        self.eye = Eye(x, y, head_direction, field_of_view)

    def look(self, environment):
        self.eye.observe(environment, self.x, self.y, self.head_direction)

    def think(self):
        self.brain.interpret(self.eye.vision)

    def move(self, step_size_move, box):
        if self.check_collision(self, box):
            self.x += step_size_move * math.cos(math.radians(self.head_direction))
            self.y += step_size_move * math.sin(math.radians(self.head_direction))

    def turn(self, step_size_turn):
        self.head_direction += step_size_turn

    def check_collision(self, box):
        for wall in box.walls:
            wx1 = wall.start_pos[0]
            wy1 = wall.start_pos[1]
            wx2 = wall.end_pos[0]
            wy2 = wall.end_pos[1]
            w_length = wall.length

            mx = self.x
            my = self.y
            mradius = self.size

            buffer = 0.1

            x_dist1 = mx - wx1
            y_dist1 = my - wy1
            dist1 = math.sqrt((x_dist1*x_dist1) + (y_dist1*y_dist1))

            x_dist2 = mx - wx2
            y_dist2 = my - wy2
            dist2 = math.sqrt((x_dist2 * x_dist2) + (y_dist2 * y_dist2))

            if dist1 <= mradius or dist2 <= mradius:
                return True

            dot = ( ((mx-wx1)*(wx2-wx1)) + ((my-wy1)*(wy2-wy1)) ) / (w_length * w_length)

            x_closest = wx1 + (dot * (wx2-wx1))
            y_closest = wy1 + (dot * (wy2-wy1))

            dot_dist_x1 = x_closest - wx1
            dot_dist_y1 = y_closest - wy1
            dot_dist1 = math.sqrt((dot_dist_x1*dot_dist_x1) + (dot_dist_y1*dot_dist_y1))

            dot_dist_x2 = x_closest - wx2
            dot_dist_y2 = y_closest - wy2
            dot_dist2 = math.sqrt((dot_dist_x2 * dot_dist_x2) + (dot_dist_y2 * dot_dist_y2))

            if w_length-buffer <= dot_dist1+dot_dist2 <= w_length+buffer:
                return True

            return False

    def draw(self):
        pass
