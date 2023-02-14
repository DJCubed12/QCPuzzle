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


def Puzzle(state=None):
    """ OURE Project prototype. """
    if state is None:
        state = F.str_to_state("|00>")
    screen = pygame.display.set_mode(SCREEN_SIZE)

    second_bit = True  # Which qubit is being operated on
    state_str = F.state_to_str(state)
    gate_str = ''

    print(f"[ Operating on 2nd qubit ]")

    while True:
        display(state, screen)

        inp = input("Enter a gate (X, Y, Z, H, CNOT), Q to quit, or S to swap: \n").upper()
        print()

        if inp == '':  # No input
            continue
        elif inp[0] == 'Q':  # Quit
            break
        elif "CNOT" in inp:  # CNOT
            if second_bit:
                gate_str = "CNOT12"
                gate = GATES["CNOT12"]
            else:
                gate_str = "CNOT21"
                gate = GATES["CNOT21"]
        elif inp[0] == 'S':  # Swap
            second_bit = not second_bit
            print(f"[ Operating on {'2nd' if second_bit else '1st'} qubit ]")
            continue
        else:
            try:  # Other gate
                gate = F.str_to_gate(inp)
            except KeyError:  # Invalid input
                continue

            if second_bit:
                gate = np.kron(GATES["I"], gate)
                gate_str = 'I' + inp
            else:
                gate = np.kron(gate, GATES["I"])
                gate_str = inp + 'I'

        print(gate_str, state_str, '=', end=' ')
        state = np.matmul(gate, state)
        state_str = F.state_to_str(state)
        print(state_str)


def display(state, screen):
    """Show 2 by 2 dot grid representation."""
    FONT = pygame.font.SysFont("Britannic Bold", 40)
    screen.fill(BLACK)

    insqrt2 = 1/np.sqrt(2)
    for i, coord in zip(state, COORDS):
        get_box = lambda r : (*(i - r for i in coord), *(i + r for i in coord))

        if isclose(i.real, 1, rel_tol=1e-15): 
            pygame.draw.rect(screen, COLOR_CODE['1'], get_box(NORM_RADIUS))
        elif isclose(i.real, -1, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['i'], get_box(NORM_RADIUS))
        elif isclose(i.imag, 1, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['-1'], get_box(NORM_RADIUS))
        elif isclose(i.imag, -1, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['-i'], get_box(NORM_RADIUS))

        elif isclose(i.real, insqrt2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['1'], get_box(NORM_RADIUS/2))
        elif isclose(i.real, -insqrt2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['i'], get_box(NORM_RADIUS/2))
        elif isclose(i.imag, insqrt2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['-1'], get_box(NORM_RADIUS/2))
        elif isclose(i.imag, -insqrt2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['-i'], get_box(NORM_RADIUS/2))

        elif isclose(i.real, 1/2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['1'], get_box(NORM_RADIUS/4))
        elif isclose(i.real, -1/2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['i'], get_box(NORM_RADIUS/4))
        elif isclose(i.imag, 1/2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['-1'], get_box(NORM_RADIUS/4))
        elif isclose(i.imag, -1/2, rel_tol=1e-15):
            pygame.draw.rect(screen, COLOR_CODE['-i'], get_box(NORM_RADIUS/4))

    # screen.blit( font.render( <text>, True, <color> ), <location> )
    screen.blit(FONT.render("|00>", True, WHITE), (30, 30))
    screen.blit(FONT.render("|01>", True, WHITE), (230, 30))
    screen.blit(FONT.render("|10>", True, WHITE), (30, 230))
    screen.blit(FONT.render("|11>", True, WHITE), (230, 230))

    for event in pygame.event.get():
        pass

    pygame.display.flip()
        

def main():
    """ High level interface """
    screen, font = init()

    try:
        while True:
            rects = []
            handle_events()
            for a, b, p in ((0, 0, '1'), (0, 1, 'i'), (1, 0, '-1'), (1, 1, '-i')):
                rects.append(draw_circles(screen, a, b, 1, p))

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


def draw_circles(screen, bot: bool, left: bool, radius: int, phase: str):
    """ Draw a state's circle according to its name, radius and phase. bot and left correspond to its position on the screen (both true => |00>). 0 <= radius <= 1. """
    centerx, centery = 9*SIZE_FACTOR, 3*SIZE_FACTOR
    if bot:
        centery += 4*SIZE_FACTOR
    if left:
        centerx -= 4*SIZE_FACTOR

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
        screen.blit(font.render(label, True, WHITE), r)
        r.y += 2*SIZE_FACTOR
    
    for color, label in reversed(button_sequence):
        r.x += 2*SIZE_FACTOR
        pygame.draw.rect(screen, color, r)
        screen.blit(font.render(label, True, WHITE), r)


class Quit(Exception):
    """ Signifies the user wants to quit. """
    pass


if __name__ == "__main__":
    print()

    main()