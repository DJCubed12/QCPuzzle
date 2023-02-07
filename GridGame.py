""" Console prototype using 4 points and symbols as a Quantum Puzzle Game for OURE. """

import numpy as np
import Funcs as F
from Constants import GATES
from math import isclose


def Puzzle(state=None):
    """ OURE Project prototype. """
    if state is None:
        state = F.str_to_state("|00>")

    second_bit = True  # Which qubit is being operated on
    state_str = F.state_to_str(state)
    gate_str = ''

    print(f"[ Operating on 2nd qubit ]")

    while True:
        display(state)

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


def display(state):
    """Show 2 by 2 dot grid representation."""
    insqrt2 = 1/np.sqrt(2)
    strings = []
    for i in state:
        if isclose(i.real, 1, rel_tol=1e-15):
            strings.append(" +1  ")
        elif isclose(i.real, -1, rel_tol=1e-15):
            strings.append(" -1  ")
        elif isclose(i.imag, 1, rel_tol=1e-15):
            strings.append(" +i  ")
        elif isclose(i.imag, -1, rel_tol=1e-15):
            strings.append(" -i  ")

        elif isclose(i.real, insqrt2, rel_tol=1e-15):
            strings.append("+1/√2")
        elif isclose(i.real, -insqrt2, rel_tol=1e-15):
            strings.append("-1/√2")
        elif isclose(i.imag, insqrt2, rel_tol=1e-15):
            strings.append("+i/√2")
        elif isclose(i.imag, -insqrt2, rel_tol=1e-15):
            strings.append("-i/√2")

        elif isclose(i.real, 1/2, rel_tol=1e-15):
            strings.append("+1/2 ")
        elif isclose(i.real, -1/2, rel_tol=1e-15):
            strings.append("-1/2 ")
        elif isclose(i.imag, 1/2, rel_tol=1e-15):
            strings.append("+i/2 ")
        elif isclose(i.imag, -1/2, rel_tol=1e-15):
            strings.append("-i/2 ")
        
        else:
            strings.append("     ")
    
    print()
    print("  |00>    |01>  ")
    print(f" {strings[0]}    {strings[1]} ", '\n')
    print(f" {strings[2]}    {strings[3]} ")
    print("  |10>  |11>  ")
    print()
        

if __name__ == "__main__":
    print()
    state = F.str_to_state(input("Please give starting state: "))
    Puzzle(state)