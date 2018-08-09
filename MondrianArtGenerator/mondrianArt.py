import pygame
from enum import Enum

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LILAC = (200, 162, 200)
colors = [WHITE, BLACK, RED, YELLOW, BLUE]

# constants
size = (640, 360)
sepWidth = 6


class Mode(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    COLOR = 3


# c2 greater than c1
class Rect():
    def __init__(self, c1, c2, colorIdx):
        self.c1 = c1
        self.c2 = c2
        self.colorIdx = colorIdx


def withinRect(pos, rect):
    if rect.c1[0] <= pos[0] <= rect.c2[0] and rect.c1[1] <= pos[1] <= rect.c2[1]:
        return True
    return False


def sepHorizontal(pos_y, rect):
    r1 = Rect((rect.c1[0], rect.c1[1]), (rect.c2[0], pos_y - sepWidth / 2), rect.colorIdx)
    r2 = Rect((rect.c1[0], pos_y + sepWidth / 2), (rect.c2[0], rect.c2[1]), rect.colorIdx)
    return [r1, r2]


def sepVertical(pos_x, rect):
    r1 = Rect((rect.c1[0], rect.c1[1]), (pos_x - sepWidth / 2, rect.c2[1]), rect.colorIdx)
    r2 = Rect((pos_x + sepWidth / 2, rect.c1[1]), (rect.c2[0], rect.c2[1]), rect.colorIdx)
    return [r1, r2]


def nextColor(rect):
    return Rect(rect.c1, rect.c2, (rect.colorIdx + 1) % len(colors))


pygame.init()
screen = pygame.display.set_mode((size[0], size[1] + 30))
pygame.display.set_caption("Mondrian Art Generator")
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)

done = False
mode = Mode.VERTICAL
rects = [Rect((0, 0), size, 0)]

while not done:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for rect in rects:
                if withinRect(pos, rect):
                    if mode == Mode.HORIZONTAL:
                        r1, r2 = sepHorizontal(pos[1], rect)
                        rects.remove(rect)
                        rects.append(r1)
                        rects.append(r2)
                    elif mode == Mode.VERTICAL:
                        r1, r2 = sepVertical(pos[0], rect)
                        rects.remove(rect)
                        rects.append(r1)
                        rects.append(r2)
                    elif mode == Mode.COLOR:
                        r = nextColor(rect)
                        rects.remove(rect)
                        rects.append(r)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                mode = Mode.HORIZONTAL
            if event.key == pygame.K_v:
                mode = Mode.VERTICAL
            if event.key == pygame.K_c:
                mode = Mode.COLOR
        if event.type == pygame.QUIT:
            done = True

    for rect in rects:
        pygame.draw.rect(screen, colors[rect.colorIdx], [rect.c1[0], rect.c1[1], rect.c2[0] - rect.c1[0], rect.c2[1] - rect.c1[1]])

    pygame.draw.rect(screen, LILAC, [0, size[1], size[0], size[1] + 30])

    modeName = ""
    if mode == Mode.VERTICAL:
        modeName = "Draw Vertical Lines"
    elif mode == Mode.HORIZONTAL:
        modeName = "Draw Horizontal Lines"
    elif mode == Mode.COLOR:
        modeName = "Change Color"
    text = font.render('Mode = %s (Change mode using keys H/V/C)' % (modeName), False, BLACK)
    screen.blit(text, (10, size[1]))

    pygame.display.flip()