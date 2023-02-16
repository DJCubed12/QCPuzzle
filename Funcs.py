""" Houses functions for state calculator. 

Notes:
    State Evolution - (gate) matrix multiplied with (state)
        gates affect qubits in order; ex: [X (X) I] |0> (X) |1> = [X|0>] (X) [I|1>]

    H gate on bell states produce non standard states
    

Numpy Funcs:
    np.kron(a, b) - Tensor/Kroneker Product
    np.matmul(a, b) - Matrix Multiplication
"""

import numpy as np

import Constants as C

import random
import re


def State_Calc():
    """ Interactive state calculator """
    state = str_to_state(input("Please give starting state: "))

    while (g := input("Provide an operation (nothing to quit): ")):
        if len(g) < 2:
            g += 'I'
        gate = str_to_gate(g)
        state = operate(state, (gate,))

def random_evolution(start_state, gates=5, rounds=1):
    """ Using the starting single qubit states, play out 'rounds' evolutions using 'gates' gates each. """
    for i in range(rounds):
        gate_list = (random_gate() for i in range(gates))
        evolve(start_state, gate_list)

def evolve(state, gate_list):
    """ Operate each set of gates on the given state successively. gate_list is a iterable of tuples of gates (max 2 per tuple). """
    for gate_set in gate_list:
        state = operate(state, gate_set)
    print()
    return state

def operate(state, gates):
    """ Operate given gates on the given state. gates should be a tuple (1 or 2). """
    if (len(gates) > 1):
        gate = np.kron(gates[0], gates[1])
    else:
        gate = gates[0]
    gatename = gate_to_str(*gates)

    end = np.matmul(gate, state)

    show(state, end, gatename)
    return end


def show(prev_state, cur_state, gate='II'):
    ps = state_to_str(prev_state)
    cs = state_to_str(cur_state)
    print(f"({gate}){ps} = {cs}")

def random_gate():
    """ Returns a random gate for a random qubit (in a 2-tuple, or 1 if a CNOT). """
    while True:  # Ensures a non-identity gate
        (name, gate) = random.choice(C.GATES.items())
        if "CNOT" in name:
            return (gate,)
        elif name == "I":
            continue
        elif random.choice((True, False)):  # Decides which bit is operated on
            return (gate, C.I)
        else:
            return (C.I, gate)


def state_to_str(state):
    for val, prefix in ((1, ''), (-1, '-'), (1j, 'i'), (-1j, '-i')):
        # Outer loop to check for global phase if matched to no standard state
        for s, name in C.state_table:
            if np.all(np.isclose(state / val, s, 0, 1e-15)):
                return prefix + name
    else:
        # If this happens often, consider multiplying by i and try again
        return str(state)

def str_to_state(inp_str):
    """ Returns the state picked by the user via console input. """
    pattern = r"([+,-]?)\s*\|([0,1,+,-]{2})>"
    matches = re.finditer(pattern, inp_str)
    # Group 1: +, -, or empty
    # Group 2: 00, 01, ..., -+, --

    end_state = np.zeros(4, complex)
    n = 0
    for m in matches:
        n += 1

        q0, q1 = m.group(2)
        state = np.kron(C.STATES[q0], C.STATES[q1])

        if m.group(1) == '-':
            state *= -1
        end_state += state

    end_state /= np.sqrt(n)
    return end_state

def gate_to_str(*args):
    """ Gates in order as they operate on qubits. """
    out = ''
    for gate in args:
        for name, g in C.GATES.items():
            if np.array_equal(gate, g):
                out += name
                break
    return out

def str_to_gate(inp_str):
    """ Raises KeyError if invalid gate input. """
    if inp_str[0] == 'C':
        if inp_str[-1] == '2':
            return C.GATES['CNOT12']
        else:
            return C.GATES['CNOT12']

    gate = 1
    for l in inp_str:  # Allows input of two qubit gates like 'IH'
        gate = np.kron(gate, C.GATES[l])
    return gate


if __name__ == "__main__":
    State_Calc()