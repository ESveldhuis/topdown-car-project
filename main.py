import pygame
import sys
import math
from road import left_edge, right_edge

pygame.init()

# ---- instellingen ----
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 100, 30)
ROAD_COLOR = (60, 60, 60)
CAR_COLOR = (0, 200, 200)
MOVE_SPEED = 3
TURN_SPEED = 3
CAR_SIZE = 6

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Car Simulation")

car_pos = [400, 85]
car_angle = 180

clock = pygame.time.Clock()

def draw_road():
    if len(left_edge) < 2 or len(right_edge) < 2:
        return
    
    road_polygon = left_edge + right_edge[::-1]
    pygame.draw.polygon(screen, ROAD_COLOR, road_polygon)

def detect_car_controls(car_pos, car_angle):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        car_angle -= TURN_SPEED
    if keys[pygame.K_RIGHT]:
        car_angle += TURN_SPEED

    if keys[pygame.K_UP]:
        rad = math.radians(car_angle)
        car_pos[0] += math.cos(rad) * MOVE_SPEED
        car_pos[1] += math.sin(rad) * MOVE_SPEED

    if keys[pygame.K_DOWN]:
        rad = math.radians(car_angle)
        car_pos[0] -= math.cos(rad) * MOVE_SPEED
        car_pos[1] -= math.sin(rad) * MOVE_SPEED

    return car_pos, car_angle

def draw_car(car_pos, car_angle):
    pygame.draw.circle(screen, CAR_COLOR, car_pos, CAR_SIZE)

    rad = math.radians(car_angle)
    tip = (
        car_pos[0] + math.cos(rad) * 15,
        car_pos[1] + math.sin(rad) * 15
    )
    pygame.draw.line(screen, (255, 0, 0), car_pos, tip, 2)

def ray_segment_intersection(ray_origin, ray_dir, point1, point2):
    origin_x, origin_y = ray_origin
    ray_x, ray_y = ray_dir
    x1, y1 = point1
    x2, y2 = point2

    edge_x = x2 - x1
    edge_y = y2 - y1

    denom = ray_x * edge_y - ray_y * edge_x
    if denom == 0:
        return None  # parallel

    t = ((x1 - origin_x) * edge_y - (y1 - origin_y) * edge_x) / denom
    u = ((x1 - origin_x) * ray_y - (y1 - origin_y) * ray_x) / denom

    if t >= 0 and 0 <= u <= 1:
        return t  # afstand langs ray
    
    return None

def calculate_distance_to_road(point, angle):
    rad = math.radians(angle)
    ray_dir = (math.cos(rad), math.sin(rad))

    min_dist = None

    for edge in (left_edge, right_edge):
        for i in range(len(edge) - 1):
            dist = ray_segment_intersection(point, ray_dir, edge[i], edge[i + 1])

            if dist is not None:
                if min_dist is None or dist < min_dist:
                    min_dist = dist

    return min_dist

running = True
while running:
    clock.tick(30)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_road()
    car_pos, car_angle = detect_car_controls(car_pos, car_angle)
    draw_car(car_pos, car_angle)
    dist = calculate_distance_to_road(car_pos, car_angle)

    if dist:
        end = (
            car_pos[0] + math.cos(math.radians(car_angle)) * dist,
            car_pos[1] + math.sin(math.radians(car_angle)) * dist
        )
        pygame.draw.line(screen, (255, 255, 0), car_pos, end, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()