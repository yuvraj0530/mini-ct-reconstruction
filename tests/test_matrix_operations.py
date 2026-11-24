
import numpy as np
import pytest

from math_engine.matrix_operations import (
    transpose_matrix,
    multiply_matrices,
    calculate_determinant,
    calculate_inverse,
    matrix_properties
)


def test_transpose_matrix():
    A = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])

    result = transpose_matrix(A)

    expected = np.array([
        [1, 4],
        [2, 5],
        [3, 6]
    ])

    assert np.array_equal(result, expected)


def test_matrix_multiplication():
    A = np.array([
        [1, 2],
        [3, 4]
    ])

    B = np.array([
        [5, 6],
        [7, 8]
    ])

    result = multiply_matrices(A, B)

    expected = np.array([
        [19, 22],
        [43, 50]
    ])

    assert np.allclose(result, expected)


def test_matrix_multiplication_invalid_dimensions():
    A = np.ones((2, 3))
    B = np.ones((2, 2))

    with pytest.raises(ValueError):
        multiply_matrices(A, B)


def test_determinant():
    A = np.array([
        [4, 7],
        [2, 6]
    ])

    result = calculate_determinant(A)

    assert np.isclose(result, 10.0)


def test_determinant_non_square():
    A = np.ones((2, 3))

    with pytest.raises(ValueError):
        calculate_determinant(A)


def test_inverse():
    A = np.array([
        [4, 7],
        [2, 6]
    ])

    result = calculate_inverse(A)

    expected = np.array([
        [0.6, -0.7],
        [-0.2, 0.4]
    ])

    assert np.allclose(result, expected)


def test_inverse_singular_matrix():
    A = np.array([
        [1, 2],
        [2, 4]
    ])

    with pytest.raises(ValueError):
        calculate_inverse(A)


def test_inverse_non_square():
    A = np.ones((2, 3))

    with pytest.raises(ValueError):
        calculate_inverse(A)


def test_matrix_properties():
    A = np.array([
        [1, 2],
        [2, 3]
    ])

    result = matrix_properties(A)

    assert result["shape"] == (2, 2)
    assert result["rows"] == 2
    assert result["columns"] == 2
    assert result["is_square"] is True
    assert result["is_symmetric"] is True


def test_matrix_properties_non_square():
    A = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])

    result = matrix_properties(A)

    assert result["is_square"] is False
    assert result["is_symmetric"] is False


def test_invalid_matrix():
    A = np.array([1, 2, 3])

    with pytest.raises(ValueError):
        transpose_matrix(A)


def test_empty_matrix():
    A = np.empty((0, 3))

    with pytest.raises(ValueError):
        matrix_properties(A)
