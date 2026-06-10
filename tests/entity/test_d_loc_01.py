import pytest

from entity.blank_coords import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given
    grid = grid_g1

    # When
    result = find_blank_coords(grid)

    # Then
    pytest.fail("RED: D-LOC-01 — find_blank_coords returns [(2,3),(4,4)] 1-index row-major")
