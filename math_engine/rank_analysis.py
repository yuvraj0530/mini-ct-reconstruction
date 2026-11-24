
import numpy as np


def analyze_matrix(A):
    """
    Analyze the rank and null space of a beam matrix.

    A: Beam matrix (2D NumPy array)
    """

    A = np.asarray(A, dtype=float)

    if A.ndim != 2:
        raise ValueError("A must be a 2D matrix.")

    if A.shape[0] == 0 or A.shape[1] == 0:
        raise ValueError("A must not be empty.")

    if not np.all(np.isfinite(A)):
        raise ValueError("A must contain finite values.")

    rows, columns = A.shape

    # Singular Value Decomposition
    U, singular_values, Vh = np.linalg.svd(
        A, full_matrices=True
    )

    # Calculate numerical rank
    if singular_values.size == 0:
        tolerance = 0.0
        rank = 0
    else:
        tolerance = (
            max(A.shape)
            * np.finfo(float).eps
            * singular_values[0]
        )
        rank = int(np.sum(singular_values > tolerance))

    # Nullity = number of columns - rank
    nullity = columns - rank

    # Null-space basis vectors
    null_space = Vh[rank:, :].T

    # Classify the system
    if rows < columns:
        system_type = "Underdetermined"
    elif rows > columns:
        system_type = "Overdetermined"
    else:
        system_type = "Square"

    # Full column rank means at most one solution
    unique_solution_possible = (rank == columns)

    return {
        "rank": rank,
        "nullity": nullity,
        "independent_measurements": rank,
        "system_type": system_type,
        "unique_solution_possible": unique_solution_possible,
        "null_space": null_space
    }
