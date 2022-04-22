from typing import Tuple

import numpy as np


def calculate_hits(m: np.ndarray, iterations: int) -> Tuple[np.ndarray, np.ndarray]:
    h = np.ones(shape=(m.shape[1], 1))
    a = np.ones(shape=(m.shape[1], 1))

    m_t = np.transpose(m)

    for i in range(iterations):
        if i > 0:
            h = np.matmul(m, a)
            h /= np.max(h)

        a = np.matmul(m_t, h)
        a /= np.max(a)

    return h, a


if __name__ == "__main__":
    matrix = np.array(
        [
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0]
        ]
    )

    h, a = calculate_hits(matrix, 10)

    print(f"Hubbiness:\n {h}")
    print(f"Authority:\n {a}")


