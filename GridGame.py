""" Console prototype using 4 points and symbols as a Quantum Puzzle Game for OURE. """

import numpy as np
import Funcs as F
from Constants import GATES


# GATES['Y'] *= 0-1j


def Puzzle(state=None):
    """ OURE Project prototype. """
    if state is None:
        state = F.str_to_state("|00>")

    second_bit = True  # Which qubit is being operated on
    state_str = F.state_to_str(state)
    gate_str = ''

    while True:
        show_grid(state, second_bit)

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
        else:
            if inp[0] == 'S':  # Swap
                second_bit = not second_bit
                print(f"Columns Swapped (Operating on {'2nd' if second_bit else '1st'} qubit)")
                continue

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

'''
def show_grid(state, std_order):
    """ Display puzzle game grid with given state. current_bit should be passed as std_order. """

    # NOTE NOTE NOTE: Problems with imaginary numbers will arrise. Change Y gate to -i * Y for this game to work

    h_bar = "   +---+---+     +---+---+ "
    v_bar = " | "
    round_margin = 0.00001

    # Inner loops: 0, 1, 2, 3 if std_order; 0, 2, 1, 3 otherwise

    for top_row in (True, False):
        print(h_bar)
        if top_row:
            print(end=" +")
        else:
            print(end=" -")

        for i in (0, 1 if std_order else 2): # First and second box
            print(end=v_bar)
            if top_row and (state[i] > round_margin): # + on top row
                print(end='0')
            elif (not top_row) and (state[i] < -round_margin): # - on bottom row
                print(end='0')
            else:
                print(end=' ')

        print(v_bar, end='   ')

        for i in (2 if std_order else 1, 3): # Third and fourth box
            print(end=v_bar)
            if top_row and (state[i] > round_margin): # + on top row
                print(end='0')
            elif (not top_row) and (state[i] < -round_margin): # - on bottom row
                print(end='0')
            else:
                print(end=' ')
        print(v_bar)
    print(h_bar)
    if std_order:
        print("   |00> |01>     |10> |11>\n")
    else:
        print("   |00> |10>     |01> |11>\n")
'''
        

if __name__ == "__main__":
    print()
    state = F.str_to_state(input("Please give starting state: "))
    Puzzle(state)