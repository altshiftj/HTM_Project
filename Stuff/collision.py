import math


def ray_collision(ray, wall):
    x1, y1 = wall.start_pos
    x2, y2 = wall.end_pos

    x3 = ray.x
    y3 = ray.y
    x4 = ray.x + ray.dir[0]
    y4 = ray.y + ray.dir[1]

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


def move_collision(animal, wall, move_dir):
    w_x1, w_y1 = wall.start_pos
    w_x2, w_y2 = wall.end_pos
    w_length = wall.length

    a_x = animal.x
    a_y = animal.y
    a_radius = animal.size

    a_x_next_forward = a_x + 0.1 * math.cos(animal.head_direction)
    a_y_next_forward = a_y + 0.1 * math.sin(animal.head_direction)
    a_x_next_back = a_x - 0.1 * math.cos(animal.head_direction)
    a_y_next_back = a_y - 0.1 * math.sin(animal.head_direction)

    buffer = a_radius

    # Distance to wall start and end points
    dist_2_w1 = dist(a_x,a_y , w_x1,w_y1)
    dist_2_w2 = dist(a_x,a_y, w_x2,w_y2)

    # Distance to wall start point at next timestep
    dist_2_w1_next = dist(a_x_next_forward,a_y_next_forward , w_x1,w_y1)
    dist_2_w2_next = dist(a_x_next_forward,a_y_next_forward , w_x2,w_y2)

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

    if a_radius >= cdist > cdist_next_forward and move_dir:
        return True
    elif a_radius >= cdist > cdist_next_back and not move_dir:
        return True

    return False


def dist(x1,y1 , x2,y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt((dx * dx) + (dy * dy))