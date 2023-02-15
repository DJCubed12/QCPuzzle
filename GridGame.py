""" Console prototype using 4 points and symbols as a Quantum Puzzle Game for OURE. """

import numpy as np
import pygame
import Funcs as F
from Constants import GATES
from math import isclose

SIZE_FACTOR = 30
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
COLOR_CODE = {
    '1': (255, 0, 0),
    'i': (0, 255, 0),
    '-1': (0, 0, 255),
    '-i': (255, 0, 255)
}


def main(state=None):
    """ High level interface """
    if state is None:
        state = F.str_to_state("|00>")
    screen, font = init()

    try:
        while True:
            rects = []
            handle_events()

            rects.extend(draw_states(screen, (0.5, 0+.5j, -0.5, 0-0.5j)))

            pygame.display.update(rects)
    except Quit:
        pygame.display.quit()
        return None

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check buttons
            pass


def draw_states(screen, state):
    """ Takes a np.array of 4 representing the quantum state and draws to screen. Returns rects needed to be updated. """
    rects = []
    for i2 in (0, 1):
        for i1 in (0, 1):
            r, p = get_statevector(state[2*i2 + i1])
            rects.append(draw_circles(screen, i1, i2, r, p))
    return rects

def get_statevector(complex_n):
    """ Returns (radius of circle for draw_circles, phase string) """
    if complex_n.real > 1e-15:
        phase = "1"
    elif complex_n.real < -1e-15:
        phase = "-1"
    elif complex_n.imag > 1e-15:
        phase = "i"
    else:
        phase = "-i"

    radius = round(abs(complex_n ** 2), 2)
    return radius, phase

def draw_circles(screen, top: bool, right: bool, radius: int, phase: str):
    """ Draw a state's circle according to its name, radius and phase. bot and left correspond to its position on the screen (both true => |11>). 0 <= radius <= 1. """
    centerx, centery = 5*SIZE_FACTOR, 7*SIZE_FACTOR
    if top:
        centery -= 4*SIZE_FACTOR
    if right:
        centerx += 4*SIZE_FACTOR

    r = pygame.draw.circle(screen, BLACK, (centerx, centery), 2*SIZE_FACTOR)
    pygame.draw.circle(screen, COLOR_CODE[phase], (centerx, centery), radius*2*SIZE_FACTOR)
    return r


def init():
    """ Create pygame window, pick starting state. """
    # state = F.str_to_state(input("Please give starting state: "))
    state = F.str_to_state("|00>")

    pygame.init()
    screen = pygame.display.set_mode((12*SIZE_FACTOR, 12*SIZE_FACTOR))
    font = pygame.font.SysFont("Britannic Bold", SIZE_FACTOR)

    screen.fill(BLACK)
    draw_frame(screen, font)

    pygame.display.flip()
    return screen, font

def draw_frame(screen, font):
    """ Draws buttons and labels. """
    r = pygame.Rect(0, 0, 2*SIZE_FACTOR, 2*SIZE_FACTOR)

    button_sequence = ((pygame.Color("coral"), "CNOT"), (pygame.Color("coral1"), "H"), (pygame.Color("coral2"), "Z"), (pygame.Color("coral3"), "Y"), (pygame.Color("coral4"), "X"))

    for color, label in button_sequence:
        pygame.draw.rect(screen, color, r)
        screen.blit(font.render(label, False, WHITE), r)
        r.y += 2*SIZE_FACTOR
    
    for color, label in reversed(button_sequence):
        r.x += 2*SIZE_FACTOR
        pygame.draw.rect(screen, color, r)
        screen.blit(font.render(label, False, WHITE), r)

    screen.blit(font.render("|00>", False, WHITE), (2*SIZE_FACTOR, 9*SIZE_FACTOR))
    screen.blit(font.render("|01>", False, WHITE), (10*SIZE_FACTOR, 9*SIZE_FACTOR))
    screen.blit(font.render("|10>", False, WHITE), (2*SIZE_FACTOR, SIZE_FACTOR/2))
    screen.blit(font.render("|11>", False, WHITE), (10*SIZE_FACTOR, SIZE_FACTOR/2))


class Quit(Exception):
    """ Signifies the user wants to quit. """
    pass


if __name__ == "__main__":
    if SIZE_FACTOR % 2:
        SIZE_FACTOR += 1

    print()

    main()