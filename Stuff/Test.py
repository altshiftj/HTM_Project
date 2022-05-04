from pygame.locals import *
import pygame
import sys
import math
import random

from collision import *

pygame.init()

# -----Options-----
WINDOW_SIZE = (1200, 800)  # Width x Height in pixels
NUM_RAYS = 3  # Must be between 1 and 360
SOLID_RAYS = False  # Can be somewhat glitchy. For best results, set NUM_RAYS to 360
NUM_WALLS = 5  # The amount of randomly generated walls
# ------------------

screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)

mx, my = (600, 400)
lastClosestPoint = (0, 0)
running = True
rays = []
walls = []
particles = []
head_direction = 0
field_of_view = 120
del_angle = 0
del_pos = 0
hit = False

class Ray:

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.dir = [math.cos(self.angle), math.sin(self.angle)]
        self.length = 0
        self.size = 10

    def update(self, del_mx, del_my, del_ang):
        self.x += del_mx * math.cos(math.radians(head_direction))
        self.y += del_my * math.sin(math.radians(head_direction))
        self.angle += math.radians(del_ang)
        self.dir = [math.cos(self.angle), math.sin(self.angle)]


    def checkCollision(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0]
        y4 = self.y + self.dir[1]

        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominator == 0:
            return None

        t = numerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collidePos = [x, y]
            return collidePos


class Wall:
    def __init__(self, start_pos, end_pos, color='white'):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.slope_x = end_pos[0] - start_pos[0]
        self.slope_y = end_pos[1] - start_pos[1]
        if self.slope_x == 0:
            self.slope = 0
        else:
            self.slope = self.slope_y / self.slope_x
        self.length = math.sqrt(self.slope_x ** 2 + self.slope_y ** 2)

    def draw(self):
        pygame.draw.line(display, self.color, self.start_pos, self.end_pos, 3)


for i in range(head_direction-int(field_of_view/2), head_direction+int(field_of_view/2),4):
    rays.append(Ray(mx, my, i))


def move_collision(ray, wall, key):
    w_x1, w_y1 = wall.start_pos
    w_x2, w_y2 = wall.end_pos
    w_length = wall.length

    a_x = ray.x
    a_y = ray.y
    a_radius = ray.size

    a_x_next_forward = a_x + 0.1 * math.cos(ray.angle)
    a_y_next_forward = a_y + 0.1 * math.sin(ray.angle)
    a_x_next_back = a_x - 0.1 * math.cos(ray.angle)
    a_y_next_back = a_y - 0.1 * math.sin(ray.angle)

    buffer = a_radius

    # Distance to wall start point
    dist_2_w1 = dist(a_x,a_y , w_x1,w_y1)

    # Distance to wall end point
    dist_2_w2 = dist(a_x,a_y, w_x2,w_y2)

    # Distance to wall start point at next timestep
    dist_2_w1_next = dist(a_x_next_forward,a_y_next_forward , w_x1,w_y1)
    dist_2_w2_next = dist(a_x_next_forward, a_y_next_forward, w_x2, w_y2)

    if (a_radius >= dist_2_w1 > dist_2_w1_next) or (a_radius >= dist_2_w2 > dist_2_w2_next):
        return True

    dot = ( ((a_x-w_x1)*(w_x2-w_x1)) + ((a_y-w_y1)*(w_y2-w_y1)) ) / (w_length * w_length)

    x_closest = w_x1 + (dot * (w_x2-w_x1))
    y_closest = w_y1 + (dot * (w_y2-w_y1))

    dot_dist1 = dist(x_closest,y_closest , w_x1,w_y1)
    dot_dist2 = dist(x_closest,y_closest , w_x2,w_y2)

    if not w_length-buffer <= dot_dist1+dot_dist2 <= w_length+buffer:
        return False

    cdist = dist(x_closest,y_closest , a_x,a_y)

    cdist_next_forward = dist(x_closest,y_closest , a_x_next_forward,a_y_next_forward)
    cdist_next_back = dist(x_closest, y_closest, a_x_next_back, a_y_next_back)

    if a_radius >= cdist > cdist_next_forward and key[pygame.K_UP]:
        return True
    elif a_radius >= cdist > cdist_next_back and key[pygame.K_DOWN]:
        return True

    return False


def drawRays(rays, walls, color='white'):
    global lastClosestPoint
    for ray in rays:
        closest = 100000
        closestPoint = None
        for wall in walls:
            intersectPoint = ray.checkCollision(wall)
            if intersectPoint is not None:
                # Get distance between ray source and intersect point
                ray_dx = ray.x - intersectPoint[0]
                ray_dy = ray.y - intersectPoint[1]
                # If the intersect point is closer than the previous closest intersect point, it becomes the closest intersect point
                ray.length = math.sqrt(ray_dx ** 2 + ray_dy ** 2)
                if (ray.length < closest):
                    closest = ray.length
                    closestPoint = intersectPoint

        if closestPoint is not None:
            pygame.draw.line(display, color, (ray.x, ray.y), closestPoint)
            ray.length = closest
            if SOLID_RAYS:
                pygame.draw.polygon(display, color, [(mx, my), closestPoint, lastClosestPoint])
                lastClosestPoint = closestPoint

    pygame.draw.circle(display, color, (rays[0].x, rays[0].y), rays[0].size)


def generateWalls():
    walls.clear()

    walls.append(Wall((0, 0), (WINDOW_SIZE[0], 0)))
    walls.append(Wall((0, 0), (0, WINDOW_SIZE[1])))
    walls.append(Wall((WINDOW_SIZE[0], 0), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
    walls.append(Wall((0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))

    # walls.append(Wall((100, 100), (1000, 100)))
    # walls.append(Wall((100, 100), (100, 1000)))
    # walls.append(Wall((1000, 100), (1000, 1000)))
    # walls.append(Wall((100, 1000), (1000, 1000)))

    for i in range(NUM_WALLS):
        start_x = random.randint(0, WINDOW_SIZE[0])
        start_y = random.randint(0, WINDOW_SIZE[1])
        end_x = random.randint(0, WINDOW_SIZE[0])
        end_y = random.randint(0, WINDOW_SIZE[1])
        walls.append(Wall((start_x, start_y), (end_x, end_y)))


def draw():
    display.fill((0, 0, 0))

    for wall in walls:
        wall.draw()

    for particle in particles:
        particle.draw()

    drawRays([ray for ray in rays], [wall for wall in walls])

    screen.blit(display, (0, 0))

    pygame.display.update()


generateWalls()
while running:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        del_angle = 1
        for ray in rays:
            ray.update(0, 0, del_angle)
        head_direction += del_angle

    if keys[pygame.K_LEFT]:
        del_angle = -1
        for ray in rays:
            ray.update(0, 0, del_angle)
        head_direction += del_angle

    if keys[pygame.K_UP]:
        for wall in walls:
            hit = move_collision(rays[int(len(rays)/2)], wall , keys)
            if hit:
                break
        if not hit:
            for ray in rays:
                del_pos = 1
                ray.update(del_pos, del_pos, 0)

    if keys[pygame.K_DOWN]:
        for wall in walls:
            hit = move_collision(rays[int(len(rays)/2)], wall, keys)
            if hit:
                break
        if not hit:
            for ray in rays:
                del_pos = -1
                ray.update(del_pos, del_pos, 0)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()


        if event.type == KEYDOWN:
            # Re-randomize walls on Space
            if event.key == pygame.K_SPACE:
                generateWalls()



    # for ray in rays:
    #     ray.update(mx, my, math.radians(del_angle))

    draw()
