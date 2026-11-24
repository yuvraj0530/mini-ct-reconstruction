
import numpy as np
import pytest

from math_engine.beam_matrix import (
    build_beam_matrix,
    simulate_measurements,
)


def test_beam_matrix_normal():
    A = build_beam_matrix((1, 1), [0], detector_count=1)

    assert A.shape == (1, 1)
    assert A[0, 0] == pytest.approx(1.0)


def test_beam_matrix_invalid_dimensions():
    with pytest.raises(ValueError):
        build_beam_matrix((0, 5), [0])


def test_beam_matrix_dimensions():
    A = build_beam_matrix((2, 2), [0, 45, 90], detector_count=3)

    assert A.shape == (9, 4)


def test_measurement_normal():
    image = np.array([[1.0]])

    A, b = simulate_measurements(
        image, [0], detector_count=1
    )

    assert A.shape == (1, 1)
    assert b.shape == (1,)
    assert b[0] == pytest.approx(1.0)


def test_measurement_invalid_image():
    image = np.array([1, 2, 3])

    with pytest.raises(ValueError):
        simulate_measurements(image, [0])


def test_measurement_against_numpy():
    image = np.array([
        [1.0, 2.0],
        [3.0, 4.0]
    ])

    A, b = simulate_measurements(
        image, [0, 45, 90], detector_count=3
    )

    expected = A @ image.flatten()

    assert np.allclose(b, expected)
