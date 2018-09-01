import sys
import pygame
import math

SIZE = (640, 640)
ANGLE = 30
LEN = 150
N = 0
MULTI = math.sqrt(2)/2

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Tree Fractal Generator')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_fractal(n, pos, angle, len, first):
    if first:
        pos_new = [pos[0], pos[1] - len]
        pygame.draw.line(screen, BLACK, pos, pos_new)
        if n < N:
            draw_fractal(n + 1, pos_new, 0, len * MULTI, False)
    else:
        pos_left = [pos[0] + len * math.sin(math.radians(angle - 30)), pos[1] - len * math.cos(math.radians(angle - 30))]
        pygame.draw.line(screen, BLACK, pos, pos_left)
        pos_right = [pos[0] + len * math.sin(math.radians(angle + 30)), pos[1] - len * math.cos(math.radians(angle + 30))]
        pygame.draw.line(screen, BLACK, pos, pos_right)
        if n < N:
            draw_fractal(n + 1, pos_left, angle - 30, len * MULTI, False)
            draw_fractal(n + 1, pos_right, angle + 30, len * MULTI, False)

screen.fill(WHITE)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            N += 1
        if event.type == pygame.QUIT:
            sys.exit()
    
    draw_fractal(0, [SIZE[0]/2, SIZE[1]], 0, LEN, True)

    pygame.display.flip()