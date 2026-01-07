import pygame
import sys
# from road import left_edge, right_edge

pygame.init()

# ---- instellingen ----
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
LEFT_COLOR = (0, 200, 0)
RIGHT_COLOR = (200, 0, 0)
LINE_WIDTH = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Topdown Road Editor")

clock = pygame.time.Clock()

left_edge = []
right_edge = []

running = True
drawing = True

# ---- main loop ----
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if drawing and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if event.button == 1:   # links
                left_edge.append(pos)

            if event.button == 3:   # rechts
                right_edge.append(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                drawing = False
                left_edge.append(left_edge[0])
                right_edge.append(right_edge[0])
                print("left_edge =", left_edge)
                print("right_edge =", right_edge)

    # ---- tekenen ----
    if len(left_edge) > 1:
        pygame.draw.lines(screen, LEFT_COLOR, False, left_edge, LINE_WIDTH)

    if len(right_edge) > 1:
        pygame.draw.lines(screen, RIGHT_COLOR, False, right_edge, LINE_WIDTH)

    pygame.display.flip()

pygame.quit()
sys.exit()
