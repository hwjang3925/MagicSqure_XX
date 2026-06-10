import pytest

from entity.constants import MAGIC_SUM
from src.validate_lines import validate_lines

PASS_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

FAIL_GRID_R1 = [
    [15, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_pass_all_ten_lines_sum_to_magic_constant():
    # Given
    grid = PASS_GRID

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-pass-01 — ok=true, status=pass, failed_lines=[]")


def test_fail_reports_wrong_line_with_id_sum_and_expected():
    # Given
    grid = FAIL_GRID_R1

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        f"RED: T-fail-01 — ok=false, status=fail, "
        f"failed_lines=[{{id:R1, sum:33, expected:{MAGIC_SUM}}}]"
    )


def test_incomplete_skips_line_validation_when_zero_present(grid_g1):
    # Given
    grid = grid_g1

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-inc-01 — ok=false, status=incomplete, failed_lines=[]")
