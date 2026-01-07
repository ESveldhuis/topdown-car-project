import pygame
import sys
from road import left_edge, right_edge

pygame.init()

# ---- instellingen ----
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 100, 30)
ROAD_COLOR = (60, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Road Editor")

def draw_road():
    if len(left_edge) < 2 or len(right_edge) < 2:
        return
    
    road_polygon = left_edge + right_edge[::-1]
    pygame.draw.polygon(screen, ROAD_COLOR, road_polygon)

running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_road()

    pygame.display.flip()

pygame.quit()
sys.exit()