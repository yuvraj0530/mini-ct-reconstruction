
import numpy as np
import pytest

from math_engine.reconstruction import reconstruct_image


def test_reconstruction_identity():
    A = np.eye(4)
    b = np.array([1.0, 2.0, 3.0, 4.0])

    result = reconstruct_image(A, b, (2, 2))

    expected = np.array([
        [1.0, 2.0],
        [3.0, 4.0]
    ])

    assert np.allclose(result, expected)


def test_reconstruction_shape():
    A = np.eye(6)
    b = np.arange(1, 7, dtype=float)

    result = reconstruct_image(A, b, (2, 3))

    assert result.shape == (2, 3)


def test_reconstruction_invalid_matrix():
    A = np.array([1, 2, 3])
    b = np.array([1, 2, 3])

    with pytest.raises(ValueError):
        reconstruct_image(A, b, (1, 3))


def test_reconstruction_dimension_mismatch():
    A = np.eye(4)
    b = np.array([1.0, 2.0])

    with pytest.raises(ValueError):
        reconstruct_image(A, b, (2, 2))


def test_reconstruction_invalid_shape():
    A = np.eye(4)
    b = np.ones(4)

    with pytest.raises(ValueError):
        reconstruct_image(A, b, (0, 2))
