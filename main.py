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

def draw_road():
    if len(left_edge) < 2 or len(right_edge) < 2:
        return
    
    road_polygon = left_edge + right_edge[::-1]
    pygame.draw.polygon(screen, ROAD_COLOR, road_polygon)

def check_for_game_over(car_pos):
    distance_to_road_edge = calculate_distance_to_road_edge(car_pos)
    if distance_to_road_edge < CAR_SIZE:
        return True
    else:
        return False

def calculate_distance_to_road_edge(car_pos):
    smalest_distance = None

    for edge in (left_edge, right_edge):
        for i in range(len(edge) - 1):
            distance_to_segment = calculate_distance_to_segment(car_pos, edge[i], edge[i + 1])
            if smalest_distance is None or distance_to_segment < smalest_distance:
                smalest_distance = distance_to_segment
    return smalest_distance

def calculate_distance_to_segment(car_pos, segment_point_1, segment_point_2):
    car_pos_x, car_pos_y = car_pos
    segment_point_1_x, segment_point_1_y = segment_point_1
    segment_point_2_x, segment_point_2_y = segment_point_2

    segment_x_diference = segment_point_2_x - segment_point_1_x
    segment_y_diference = segment_point_2_y - segment_point_1_y
    car_pos_point_1_x_diference = car_pos_x - segment_point_1_x
    car_pos_point_1_y_diference = car_pos_y - segment_point_1_y

    segment_length_square = segment_x_diference*segment_x_diference + segment_y_diference*segment_y_diference
    if segment_length_square == 0: #if segment length == 0
        return math.hypot(car_pos_point_1_x_diference, car_pos_point_1_y_diference)

    t = (car_pos_point_1_x_diference*segment_x_diference + car_pos_point_1_y_diference*segment_y_diference) / segment_length_square
    t = max(0, min(1, t))

    closest_x = segment_point_1_x + t * segment_x_diference
    closest_y = segment_point_1_y + t * segment_y_diference

    return math.hypot(car_pos_x - closest_x, car_pos_y - closest_y)

def move_forward(personal_car_pos, personal_car_angle, personal_score):
    personal_score += 1
    rad = math.radians(personal_car_angle)
    personal_car_pos[0] += math.cos(rad) * MOVE_SPEED
    personal_car_pos[1] += math.sin(rad) * MOVE_SPEED
    game_over = check_for_game_over(personal_car_pos)
    return personal_car_pos, personal_car_angle, personal_score, game_over

def move_back(personal_car_pos, personal_car_angle, personal_score):
    personal_score -= 1
    rad = math.radians(personal_car_angle)
    personal_car_pos[0] -= math.cos(rad) * MOVE_SPEED
    personal_car_pos[1] -= math.sin(rad) * MOVE_SPEED
    game_over = check_for_game_over(personal_car_pos)
    return personal_car_pos, personal_car_angle, personal_score, game_over

def turn_right(personal_car_pos, personal_car_angle, personal_score):
    personal_car_angle += TURN_SPEED
    game_over = check_for_game_over(personal_car_pos)
    return personal_car_pos, personal_car_angle, personal_score, game_over

def turn_left(personal_car_pos, personal_car_angle, personal_score):
    personal_car_angle -= TURN_SPEED
    game_over = check_for_game_over(personal_car_pos)
    return personal_car_pos, personal_car_angle, personal_score, game_over

def detect_car_controls(car_pos, car_angle, score):
    game_over = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        car_pos, car_angle, score, game_over = turn_left(car_pos, car_angle, score)
    if keys[pygame.K_RIGHT]:
        car_pos, car_angle, score, game_over = turn_right(car_pos, car_angle, score)

    if keys[pygame.K_UP]:
        car_pos, car_angle, score, game_over = move_forward(car_pos, car_angle, score)

    if keys[pygame.K_DOWN]:
        car_pos, car_angle, score, game_over = move_back(car_pos, car_angle, score)
    return car_pos, car_angle, score, game_over

def draw_car(personal_car_pos, personal_car_angle):
    pygame.draw.circle(screen, CAR_COLOR, personal_car_pos, CAR_SIZE)

    rad = math.radians(personal_car_angle)
    tip = (
        personal_car_pos[0] + math.cos(rad) * 15,
        personal_car_pos[1] + math.sin(rad) * 15
    )
    pygame.draw.line(screen, (255, 0, 0), personal_car_pos, tip, 2)

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

def draw_ray(angle, dist, car_pos):
    if dist:
        end = (
            car_pos[0] + math.cos(math.radians(angle)) * dist,
            car_pos[1] + math.sin(math.radians(angle)) * dist
        )
        pygame.draw.line(screen, (255, 255, 0), car_pos, end, 2)

def get_input(personal_car_pos, personal_car_angle):
    input_values = []
    ray = -40
    while ray <= 40:
        dist = calculate_distance_to_road(personal_car_pos, personal_car_angle + ray)
        input_values.append(dist)
        draw_ray(personal_car_angle + ray, dist, personal_car_pos)
        ray += 20
    return input_values

def render_game(personal_car_pos, personal_car_angle):
    screen.fill(BG_COLOR)
    draw_road()
    draw_car(personal_car_pos, personal_car_angle)
    pygame.display.flip()
    return get_input(personal_car_pos, personal_car_angle)

if __name__ == "__main__":
    clock = pygame.time.Clock()
    car_pos = [400, 85]
    car_angle = 180
    score = 0
    game_over = False
    running = True
    while running and not game_over:
        clock.tick(30)
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_road()
        car_pos, car_angle, score, game_over = detect_car_controls(car_pos, car_angle, score)
        draw_car(car_pos, car_angle)

        pygame.display.flip()

    pygame.quit()
    sys.exit()