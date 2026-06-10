import pytest

# G1: partial 4×4 grid — blanks at 1-indexed (2,3) and (4,4)
G1 = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]


@pytest.fixture
def grid_g1():
    return [row[:] for row in G1]
