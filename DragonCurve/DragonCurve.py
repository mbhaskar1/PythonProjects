import sys
import pygame
import numpy
import math
from pygame.locals import *

A = numpy.matrix('0, 0, 1;0, 1, 1')
size = (640, 640)
scale = 2
centerX = size[0]/3
centerY = size[1]/3

# Transformations
Rotate45 = (1/math.sqrt(2)) * numpy.matrix('1, -1; 1, 1')
Rotate90 = numpy.matrix('0, -1; 1, 0')


def next_step(m):
    m = m - m[:, -1]
    m = numpy.matmul(Rotate45, m)
    n = numpy.matmul(Rotate90, numpy.flip(m[:, 0:-1], axis=1))
    m = numpy.concatenate((m, n), axis=1)
    return m


def draw(m, surface, c):
    for i in range(0, m.shape[1] - 1):
        pygame.draw.line(surface, c,
                         [centerX + scale * m[0, i], centerY - scale * m[1, i]],
                         [centerX + scale * m[0, i + 1], centerY - scale * m[1, i + 1]],
                         1)


# Initialise screen
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dragon Curve Generator')

WHITE = (255, 255, 255)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            A = next_step(A)
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(WHITE)

    draw(A, screen, (0, 0, 0))

    pygame.display.flip()

