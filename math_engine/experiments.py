
import numpy as np

from math_engine.beam_matrix import simulate_measurements
from math_engine.reconstruction import reconstruct_image
from math_engine.rank_analysis import analyze_matrix


def run_beam_count_experiment(image, angle_counts, detector_count):
    """
    Compare reconstruction quality using different numbers
    of projection angles.
    """

    results = []

    for angle_count in angle_counts:

        angles = np.linspace(
            0,
            180,
            angle_count,
            endpoint=False
        )

        A, b = simulate_measurements(
            image,
            angles,
            detector_count
        )

        reconstructed = reconstruct_image(
            A,
            b,
            image.shape
        )

        analysis = analyze_matrix(A)

        mse = float(
            np.mean((image - reconstructed) ** 2)
        )

        results.append({
            "angles": angle_count,
            "beams": A.shape[0],
            "rank": analysis["rank"],
            "nullity": analysis["nullity"],
            "mse": mse
        })

    return results
