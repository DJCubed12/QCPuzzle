""" Constants for State Calculator. """

import numpy as np

# Basic states
Q0 = np.array((1, 0), dtype = complex)  # |0>
Q1 = np.array((0, 1), dtype = complex)  # |1>
QP = np.array((1, 1), dtype = complex) / np.sqrt(2)   # |+>
QM = np.array((1, -1), dtype = complex) / np.sqrt(2)  # |->

STATES = {
    '0': Q0,
    '1': Q1,
    '+': QP,
    '-': QM
}

# Single qubit gates
I = np.array(((1, 0), (0, 1)), dtype = complex)
X = np.array(((0, 1), (1, 0)), dtype = complex)
Y = np.array(((0, -1j), (1j, 0)), dtype = complex)
Z = np.array(((1, 0), (0, -1)), dtype = complex)
H = np.array(((1, 1), (1, -1)), dtype = complex) / np.sqrt(2)
S = np.array(((1, 0), (0, 1j)), dtype = complex)

# Two qubit gates
CNOT12 = np.array(((1, 0, 0, 0),
                   (0, 1, 0, 0),
                   (0, 0, 0, 1),
                   (0, 0, 1, 0)), dtype = complex)
CNOT21 = np.array(((1, 0, 0, 0),
                   (0, 0, 0, 1),
                   (0, 0, 1, 0),
                   (0, 1, 0, 0)), dtype = complex)

GATES = {
    'I': I,
    'X': X,
    'Y': Y,
    'Z': Z,
    'H': H,
    'S': S,
    'CNOT12': CNOT12,
    'CNOT21': CNOT21
}

# Mixed states
Q00P11 = np.matmul(CNOT12, np.kron(QP, Q0))
Q00M11 = np.matmul(CNOT12, np.kron(QM, Q0))
Q01P10 = np.matmul(CNOT12, np.kron(QP, Q1))
Q01M10 = np.matmul(CNOT12, np.kron(QM, Q1))

state_table = (
    (np.kron(Q0, Q0), "|00>"),
    (np.kron(Q0, Q1), "|01>"),
    (np.kron(Q0, QP), "|0+>"),
    (np.kron(Q0, QM), "|0->"),

    (np.kron(Q1, Q0), "|10>"),
    (np.kron(Q1, Q1), "|11>"),
    (np.kron(Q1, QP), "|1+>"),
    (np.kron(Q1, QM), "|1->"),

    (np.kron(QP, Q0), "|+0>"),
    (np.kron(QP, Q1), "|+1>"),
    (np.kron(QP, QP), "|++>"),
    (np.kron(QP, QM), "|+->"),

    (np.kron(QM, Q0), "|-0>"),
    (np.kron(QM, Q1), "|-1>"),
    (np.kron(QM, QP), "|-+>"),
    (np.kron(QM, QM), "|-->"),

    (np.matmul(CNOT12, np.kron(QP, Q0)), "|Φ⁺>"),
    (np.matmul(CNOT12, np.kron(QM, Q0)), "|Φ⁻>"),
    (np.matmul(CNOT12, np.kron(QP, Q1)), "|Ψ⁺>"),
    (np.matmul(CNOT12, np.kron(QM, Q1)), "|Ψ⁻>")
)

if __name__ == "__main__":
    print(np.kron(1, I))