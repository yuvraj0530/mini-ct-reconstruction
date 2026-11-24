
import numpy as np
import pytest

from math_engine.rank_analysis import analyze_matrix


def test_rank_identity_matrix():
    A = np.eye(3)

    result = analyze_matrix(A)

    assert result["rank"] == 3
    assert result["nullity"] == 0
    assert result["unique_solution_possible"] is True


def test_underdetermined_matrix():
    A = np.array([
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 1.0]
    ])

    result = analyze_matrix(A)

    assert result["system_type"] == "Underdetermined"
    assert result["rank"] == 2
    assert result["nullity"] == 1
    assert result["unique_solution_possible"] is False


def test_overdetermined_matrix():
    A = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0]
    ])

    result = analyze_matrix(A)

    assert result["system_type"] == "Overdetermined"
    assert result["rank"] == 2
    assert result["nullity"] == 0
    assert result["unique_solution_possible"] is True


def test_null_space():
    A = np.array([
        [1.0, 1.0]
    ])

    result = analyze_matrix(A)
    null_space = result["null_space"]

    assert null_space.shape == (2, 1)
    assert np.allclose(A @ null_space, 0)


def test_invalid_matrix_dimensions():
    A = np.array([1, 2, 3])

    with pytest.raises(ValueError):
        analyze_matrix(A)


def test_empty_matrix():
    A = np.empty((0, 3))

    with pytest.raises(ValueError):
        analyze_matrix(A)
