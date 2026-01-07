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

    pygame.display.flip()

pygame.quit()
sys.exit()