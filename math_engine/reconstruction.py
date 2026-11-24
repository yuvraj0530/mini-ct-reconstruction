
import numpy as np


def reconstruct_image(A, b, image_shape):
    """
    Reconstruct an image using the least-squares method.

    A: Beam matrix
    b: Measurement vector
    image_shape: Original image dimensions (height, width)
    """

    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)

    if A.ndim != 2:
        raise ValueError("A must be a 2D matrix.")

    if b.ndim != 1:
        raise ValueError("b must be a 1D vector.")

    if A.shape[0] != b.shape[0]:
        raise ValueError("A and b dimensions do not match.")

    if not np.all(np.isfinite(A)) or not np.all(np.isfinite(b)):
        raise ValueError("A and b must contain finite values.")

    height, width = image_shape

    if height <= 0 or width <= 0:
        raise ValueError("Image dimensions must be positive.")

    if A.shape[1] != height * width:
        raise ValueError("Image shape does not match matrix columns.")

    # Solve the least-squares problem.
    reconstructed_vector, residuals, rank, singular_values = (
        np.linalg.lstsq(A, b, rcond=None)
    )

    # Convert the vector back into a 2D image.
    reconstructed_image = reconstructed_vector.reshape(
        height, width
    )

    return reconstructed_image
