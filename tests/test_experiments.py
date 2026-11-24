
import numpy as np

from math_engine.experiments import run_beam_count_experiment


def test_beam_count_experiment_returns_results():
    image = np.zeros((8, 8))
    image[2:6, 2:6] = 1

    results = run_beam_count_experiment(
        image,
        angle_counts=[4, 8, 12],
        detector_count=8
    )

    assert len(results) == 3


def test_experiment_contains_required_metrics():
    image = np.zeros((8, 8))
    image[2:6, 2:6] = 1

    results = run_beam_count_experiment(
        image,
        angle_counts=[4, 8],
        detector_count=8
    )

    required_keys = {
        "angles",
        "beams",
        "rank",
        "nullity",
        "mse"
    }

    for result in results:
        assert required_keys.issubset(result.keys())


def test_beam_count_experiment_values_are_valid():
    image = np.zeros((8, 8))
    image[2:6, 2:6] = 1

    results = run_beam_count_experiment(
        image,
        angle_counts=[4, 8],
        detector_count=8
    )

    for result in results:
        assert result["beams"] > 0
        assert result["rank"] >= 0
        assert result["nullity"] >= 0
        assert result["mse"] >= 0
