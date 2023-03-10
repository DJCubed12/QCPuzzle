""" Console prototype using 4 points and symbols as a Quantum Puzzle Game for OURE. """

import numpy as np
import pygame
from Funcs import state_to_str
from Constants import GATES, Q0  # Dictionary of basic gates, |0> state

SIZE_FACTOR = 40
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
COLOR_CODE = {
    '1': pygame.Color("orange2"),
    'i': pygame.Color("yellow1"),
    '-1': pygame.Color("limegreen"),
    '-i': pygame.Color("deepskyblue3")
}


def main():
    """ High level interface """
    screen = init()
    font = pygame.font.SysFont("Britannic Bold", int(5*SIZE_FACTOR/8))

    state = np.kron(Q0, Q0)
    state_str = "|00>"
    pygame.display.update(draw_state(screen, state))

    try:
        while True:
            try:
                # Returns (new_state, gate_str) if state was changed, else None (would raises TypeError)
                new_state, gate_str = handle_events(state)  
                rects = draw_state(screen, new_state)

                label_rect = pygame.Rect(5*SIZE_FACTOR, 11.5*SIZE_FACTOR, 4*SIZE_FACTOR, SIZE_FACTOR/2)
                rects.append(label_rect)

                pygame.draw.rect(screen, BLACK, label_rect)

                math_txt = gate_str + state_str
                state = new_state
                state_str = state_to_str(state)
                math_txt += " = " + state_str

                screen.blit(font.render(math_txt, False, WHITE), label_rect)

                pygame.display.update(rects)
            except TypeError:
                pass
    except Quit:
        pygame.display.quit()

def handle_events(state):
    """ Handles gate buttons and their appropriate operations. Returns (new state, string representation of gate applied). Raises Quit if user closes window. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Quit()
        
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                raise Quit()
            elif event.key == pygame.K_r:  # Reset
                return np.kron(Q0, Q0), '[RESET]'
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check buttons
            x, y = pygame.mouse.get_pos()
            if x <= 2*SIZE_FACTOR:  # LEFT SIDE
                first_q = True
                if y < 2*SIZE_FACTOR:     # CNOT
                    gate_str = "CNOT12"
                elif y < 4*SIZE_FACTOR:   # H
                    gate_str = "H"
                elif y < 6*SIZE_FACTOR:   # S
                    gate_str = "S"
                elif y < 8*SIZE_FACTOR:   # Z
                    gate_str = "Z"
                elif y < 10*SIZE_FACTOR:   # Y
                    gate_str = "Y"
                elif y <= 12*SIZE_FACTOR: # X
                    gate_str = "X"
                else:  # Bot left corner: multiply all by i
                    return 1j * state, "i * "
            elif y >= 10*SIZE_FACTOR:  # BOTTOM ROW
                first_q = False
                # Bottom left corner is caught under above if statement
                if x < 4*SIZE_FACTOR:     # X
                    gate_str = "X"
                elif x < 6*SIZE_FACTOR:   # Y
                    gate_str = "Y"
                elif x < 8*SIZE_FACTOR:   # Z
                    gate_str = "Z"
                elif x < 10*SIZE_FACTOR:  # S
                    gate_str = "S"
                elif x < 12*SIZE_FACTOR:  # H
                    gate_str = "H"
                else:                     # CNOT
                    gate_str = "CNOT21"
            else:  # MIDDLE OF SCREEN
                continue

            # Only mouse presses on actual buttons make it to this point
            if len(gate_str) < 2:
                if first_q:
                    gate = np.kron(GATES[gate_str], GATES['I'])
                    gate_str += 'I'
                else:
                    gate = np.kron(GATES['I'], GATES[gate_str])
                    gate_str = 'I' + gate_str
            else:
                gate = GATES[gate_str]
            
            return np.matmul(gate, state), gate_str


def draw_state(screen, state):
    """ Takes a np.array of 4 representing the quantum state and draws to screen. Returns pygame.Rects needed to be updated. """
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

def draw_circles(screen, right: bool, top: bool, radius: int, phase: str):
    """ Draw a statevector's circle according to its position, radius and phase. right and top correspond to its position on the screen (both true => |11>). 0 <= radius <= 1. """
    centerx, centery = 5*SIZE_FACTOR, 9*SIZE_FACTOR
    if right:
        centerx += 6*SIZE_FACTOR
    if top:
        centery -= 6*SIZE_FACTOR

    r = pygame.draw.circle(screen, BLACK, (centerx, centery), 2*SIZE_FACTOR)
    pygame.draw.circle(screen, COLOR_CODE[phase], (centerx, centery), radius*2*SIZE_FACTOR)
    return r


def init():
    """ Set up pygame window and static UI elements. Returns pygame.Surface of the window. """
    pygame.init()
    screen = pygame.display.set_mode((14*SIZE_FACTOR, 14*SIZE_FACTOR))
    font = pygame.font.SysFont("Britannic Bold", SIZE_FACTOR)

    screen.fill(BLACK)
    draw_frame(screen, font)

    pygame.display.flip()
    return screen

def draw_frame(screen, font):
    """ Draws buttons and labels. """
    r = pygame.Rect(0, 0, 2*SIZE_FACTOR, 2*SIZE_FACTOR)

    button_sequence = ((pygame.Color("green"), "CNOT"),
                       (pygame.Color("coral"), "H"),
                       (pygame.Color("coral1"), "S"),
                       (pygame.Color("coral2"), "Z"),
                       (pygame.Color("coral3"), "Y"),
                       (pygame.Color("coral4"), "X"))

    for color, label in button_sequence:
        pygame.draw.rect(screen, color, r)
        screen.blit(font.render(label, False, WHITE), r)
        r.y += 2*SIZE_FACTOR
    
    pygame.draw.rect(screen, pygame.Color("darkred"), r)
    screen.blit(font.render("i", False, WHITE), r)

    for color, label in reversed(button_sequence):
        r.x += 2*SIZE_FACTOR
        pygame.draw.rect(screen, color, r)
        screen.blit(font.render(label, False, WHITE), r)

    screen.blit(font.render("|00>", False, WHITE), (2*SIZE_FACTOR, 11*SIZE_FACTOR))
    screen.blit(font.render("|01>", False, WHITE), (12*SIZE_FACTOR, 11*SIZE_FACTOR))
    screen.blit(font.render("|10>", False, WHITE), (2*SIZE_FACTOR, SIZE_FACTOR/2))
    screen.blit(font.render("|11>", False, WHITE), (12*SIZE_FACTOR, SIZE_FACTOR/2))


class Quit(Exception):
    """ Signifies the user wants to quit. """
    pass


if __name__ == "__main__":
    SIZE_FACTOR -= SIZE_FACTOR % 2  # Ensures even number
    main()