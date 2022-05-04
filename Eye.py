from Ray import *


class Eye:

    def __init__(self, x, y, direction, field_of_view):
        self.vision = []
        self.field_of_view = field_of_view
        for i in range(direction - int(field_of_view / 2), direction + int(field_of_view / 2)):
            self.vision.append(Ray(x, y, math.radians(i)))

    def observe(self, walls, x, y, direction):
        i = 0
        for ray in self.vision:
            ray.update(x, y, direction-int(self.field_of_view/2)+i)
            i += 1
            closest = 100000
            closest_point = None
            for wall in walls:
                intersect_point = ray.check_collision(wall)
                if intersect_point is not None:
                    # Get distance between ray source and intersect point
                    ray_dx = ray.x - intersect_point[0]
                    ray_dy = ray.y - intersect_point[1]
                    ray.length = math.sqrt(ray_dx ** 2 + ray_dy ** 2)
                    # If the intersection is closer than the previous closest intersect point,
                    # it becomes the closest intersection
                    if ray.length < closest:
                        closest = ray.length
                        closest_point = intersect_point
            if closest_point is not None:
                ray.length = closest
