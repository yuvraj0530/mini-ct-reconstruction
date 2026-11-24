
import numpy as np


def _validate_matrix(A):
    """Convert input into a valid 2D matrix."""

    A = np.asarray(A, dtype=float)

    if A.ndim != 2:
        raise ValueError("Input must be a 2D matrix.")

    if A.shape[0] == 0 or A.shape[1] == 0:
        raise ValueError("Matrix must not be empty.")

    if not np.all(np.isfinite(A)):
        raise ValueError("Matrix must contain finite values.")

    return A


def transpose_matrix(A):
    """Return the transpose of a matrix."""

    A = _validate_matrix(A)

    return A.T


def multiply_matrices(A, B):
    """Multiply two matrices."""

    A = _validate_matrix(A)
    B = _validate_matrix(B)

    if A.shape[1] != B.shape[0]:
        raise ValueError(
            "Matrix dimensions are not compatible for multiplication."
        )

    return A @ B


def calculate_determinant(A):
    """Calculate the determinant of a square matrix."""

    A = _validate_matrix(A)

    if A.shape[0] != A.shape[1]:
        raise ValueError("Determinant requires a square matrix.")

    return float(np.linalg.det(A))


def calculate_inverse(A):
    """Calculate the inverse of a nonsingular square matrix."""

    A = _validate_matrix(A)

    if A.shape[0] != A.shape[1]:
        raise ValueError("Inverse requires a square matrix.")

    try:
        return np.linalg.inv(A)
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is singular and has no inverse.")


def matrix_properties(A):
    """Return basic properties of a matrix."""

    A = _validate_matrix(A)

    rows, columns = A.shape

    return {
        "shape": A.shape,
        "rows": rows,
        "columns": columns,
        "is_square": rows == columns,
        "is_symmetric": (
            rows == columns and np.allclose(A, A.T)
        )
    }
