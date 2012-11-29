import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
import abstractled


import pygame
pygame.init()

black = (0, 0, 0)

def scale_rect(r):
    """
    Scale tuple with len(r) == 4 to screen
    """
    # Scaling
    r = list(r)
    r[0], r[2] = r[0] * sx, r[2] * sx
    r[1], r[3] = r[1] * sy, r[3] * sy
    r = tuple(r)
    return r


class VirtualLedScreen(abstractled.AbstractLed):
    def __init__(self, dimension=(12,10), ssize=(600, 500)):
        abstractled.AbstractLed.__init__(self, dimension)
        self.screen = pygame.display.set_mode(ssize)
        self.screen.fill(black)
        self.sx, self.sy = float(ssize[0]) / dimension[0], \
            float(ssize[1]) / dimension[1]

    def draw(self):
        surf = pygame.display.get_surface()
        for x in xrange(self.w):
            for y in xrange(self. h):
                i = x + y * self.w
                r = (x * self.sx, y * self.sy, self.sx, self.sy)
                r = pygame.Rect(r)
                pygame.draw.rect(surf, self.buf[i], r)

    def push(self):
        self.draw()
        pygame.display.flip()
        self.screen.fill(black)