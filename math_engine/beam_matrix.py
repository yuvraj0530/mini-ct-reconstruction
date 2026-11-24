
import math
import numpy as np


def _line_pixel_intersection_length(
    x0, y0, dx, dy,
    x_min, x_max, y_min, y_max
):
    """Calculate how much of a beam passes through one pixel."""

    t_min = -float("inf")
    t_max = float("inf")

    # Check intersection with the vertical boundaries.
    if abs(dx) < 1e-12:
        if x0 < x_min or x0 > x_max:
            return 0.0
    else:
        tx1 = (x_min - x0) / dx
        tx2 = (x_max - x0) / dx

        t_min = max(t_min, min(tx1, tx2))
        t_max = min(t_max, max(tx1, tx2))

    # Check intersection with the horizontal boundaries.
    if abs(dy) < 1e-12:
        if y0 < y_min or y0 > y_max:
            return 0.0
    else:
        ty1 = (y_min - y0) / dy
        ty2 = (y_max - y0) / dy

        t_min = max(t_min, min(ty1, ty2))
        t_max = min(t_max, max(ty1, ty2))

    return max(0.0, t_max - t_min)


def build_beam_matrix(image_shape, angles, detector_count=None):
    """Build the CT beam matrix A."""

    height, width = image_shape

    if height <= 0 or width <= 0:
        raise ValueError("Image dimensions must be positive.")

    angles = np.asarray(list(angles), dtype=float)

    if angles.ndim != 1 or not np.all(np.isfinite(angles)):
        raise ValueError("Angles must be a finite one-dimensional sequence.")

    if detector_count is None:
        radius = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)
        detector_count = max(2, math.ceil(2 * radius) + 1)

    if (
        not isinstance(detector_count, (int, np.integer))
        or isinstance(detector_count, (bool, np.bool_))
        or detector_count <= 0
    ):
        raise ValueError("Detector count must be a positive integer.")

    radius = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)

    if detector_count == 1:
        offsets = np.array([0.0])
    else:
        offsets = np.linspace(-radius, radius, detector_count)

    A = np.zeros(
        (len(angles) * detector_count, height * width),
        dtype=float
    )

    beam_index = 0

    for angle in angles:
        theta = math.radians(angle)

        # Normal and direction of the beam.
        nx = math.cos(theta)
        ny = math.sin(theta)

        dx = -ny
        dy = nx

        for offset in offsets:

            # A point on the beam.
            x0 = offset * nx
            y0 = offset * ny

            pixel_index = 0

            for row in range(height):
                for col in range(width):

                    # Pixel boundaries.
                    x_min = col - width / 2
                    x_max = x_min + 1

                    y_max = height / 2 - row
                    y_min = y_max - 1

                    length = _line_pixel_intersection_length(
                        x0, y0, dx, dy,
                        x_min, x_max,
                        y_min, y_max
                    )

                    A[beam_index, pixel_index] = length

                    pixel_index += 1

            beam_index += 1

    return A


def simulate_measurements(image, angles, detector_count=None):
    """Simulate CT measurements using A multiplied by image x."""

    image = np.asarray(image, dtype=float)

    if image.ndim != 2 or image.size == 0:
        raise ValueError("Image must be a non-empty 2D array.")

    if not np.all(np.isfinite(image)):
        raise ValueError("Image values must be finite.")

    A = build_beam_matrix(
        image.shape,
        angles,
        detector_count
    )

    x = image.flatten()

    b = A @ x

    return A, b
