import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from math_engine.beam_matrix import simulate_measurements
from math_engine.reconstruction import reconstruct_image
from math_engine.rank_analysis import analyze_matrix
from db.database import initialize_database, save_scan, get_all_scans
from math_engine.experiments import run_beam_count_experiment


st.set_page_config(
    page_title="Mini CT Scan Reconstruction",
    page_icon="🩻",
    layout="wide"
)
initialize_database()

st.title("Mini CT Scan Reconstruction")
st.caption("A 2D CT simulation using Linear Algebra")

st.sidebar.header("Scan Configuration")

phantom_name = st.sidebar.selectbox(
    "Select Phantom",
    ["Square", "Circle", "Custom"]
)

image_size = st.sidebar.slider(
    "Image Size",
    min_value=8,
    max_value=32,
    value=16,
    step=4
)

projection_angles = st.sidebar.slider(
    "Projection Angles",
    min_value=4,
    max_value=36,
    value=12,
    step=4
)

detector_count = st.sidebar.slider(
    "Number of Detectors",
    min_value=4,
    max_value=40,
    value=16,
    step=4
)
noise_level = st.sidebar.slider(
    "Measurement Noise Level",
    min_value=0.0,
    max_value=0.10,
    value=0.0,
    step=0.01
)


def create_phantom(name, size):
    """Generate a simple 2D phantom image."""

    image = np.zeros((size, size), dtype=float)

    center = size // 2

    if name == "Square":
        start = size // 4
        end = 3 * size // 4
        image[start:end, start:end] = 1.0

    elif name == "Circle":
        y, x = np.ogrid[:size, :size]
        mask = (
            (x - center) ** 2 + (y - center) ** 2
            <= (size // 4) ** 2
        )
        image[mask] = 1.0

    elif name == "Custom":
        image[center - 2:center + 2, center - 4:center + 4] = 1.0

    return image



if st.sidebar.button("Run CT Scan"):

    image = create_phantom(phantom_name, image_size)

    angles = np.linspace(
        0, 180, projection_angles, endpoint=False
    )

    A, b = simulate_measurements(
        image,
        angles,
        detector_count
    )
    noise = np.random.normal(
    loc=0.0,
    scale=noise_level * np.max(np.abs(b)),
    size=b.shape
)

    b_noisy = b + noise
    reconstructed = reconstruct_image(
        A,
        b_noisy,
        image.shape
    )
    mse = np.mean((image - reconstructed) ** 2)

    rmse = np.sqrt(mse)

    relative_error = (
    np.linalg.norm(image - reconstructed)
    / np.linalg.norm(image)
)

    analysis = analyze_matrix(A)

    scan_id = save_scan(
        image_name=phantom_name,
        image_height=image.shape[0],
        image_width=image.shape[1],
        projection_angles=len(angles),
        detector_count=detector_count,
        matrix_rank=analysis["rank"],
        phantom_type=phantom_name,
        measurements=b_noisy,
        reconstructed_image=reconstructed,
        mse=mse,
        rmse=rmse
    )
    st.success(f"Scan saved successfully! Scan ID: {scan_id}")

    st.session_state["image"] = image
    st.session_state["measurements_clean"] = b
    st.session_state["measurements_noisy"] = b_noisy
    st.session_state["reconstructed"] = reconstructed
    st.session_state["analysis"] = analysis
    st.session_state["beam_matrix"] = A
    st.session_state["mse"] = mse
    st.session_state["rmse"] = rmse
    st.session_state["relative_error"] = relative_error
    st.session_state["noise_level"] = noise_level
if "image" in st.session_state:
    st.header("Measurement Comparison")

    clean = st.session_state["measurements_clean"]
    noisy = st.session_state["measurements_noisy"]

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(clean, label="Clean Measurements")
    ax.plot(noisy, label="Noisy Measurements", alpha=0.7)

    ax.set_xlabel("Measurement Index")
    ax.set_ylabel("Measurement Value")
    ax.set_title("Clean vs Noisy CT Measurements")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)
    st.header("Scan Results")

    col1, col2 = st.columns(2) 

    with col1:
        st.subheader("Original Phantom")

        fig, ax = plt.subplots()
        ax.imshow(
            st.session_state["image"],
            cmap="gray",
            interpolation="nearest"
        )
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.subheader("Reconstructed Image")

        fig, ax = plt.subplots()
        ax.imshow(
            st.session_state["reconstructed"],
            cmap="gray",
            interpolation="nearest"
        )
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)

    st.header("Matrix Analysis")

    analysis = st.session_state["analysis"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Matrix Rank", analysis["rank"])
    col2.metric("Nullity", analysis["nullity"])
    col3.metric(
        "Independent Measurements",
        analysis["independent_measurements"]
    )

    st.write(
        "**System Type:**",
        analysis["system_type"]
    )

    st.write(
        "**Unique Solution Possible:**",
        analysis["unique_solution_possible"]
    )
    st.header("Reconstruction Quality")

    col1, col2, col3 = st.columns(3)

    col1.metric(
    "Mean Squared Error (MSE)",
    f"{st.session_state['mse']:.6f}"
    )

    col2.metric(
    "Root Mean Squared Error (RMSE)",
    f"{st.session_state['rmse']:.6f}"
    )

    col3.metric(
    "Relative Error",
    f"{st.session_state['relative_error']:.6f}"
)

    st.header("Projection Measurements")

    st.line_chart(st.session_state["measurements_noisy"])

    st.header("Beam Matrix")

    st.write(st.session_state["beam_matrix"])

else:
    st.info("Configure your scan using the sidebar and click Run CT Scan.")


st.divider()

st.header("Scan History")

scan_history = get_all_scans()

if scan_history:
    history_data = [dict(scan) for scan in scan_history]

    st.dataframe(
        history_data,
        use_container_width=True
    )
else:
    st.info("No previous scans found.")


st.divider()

st.header("Beam Count Experiment")

st.write(
    "Compare reconstruction quality using different "
    "numbers of projection angles."
)

if st.button("Run Beam Count Experiment"):

    experiment_image = create_phantom("Square", 16)

    angle_counts = [4, 8, 12, 16, 20, 24, 28, 32, 36]

    experiment_results = run_beam_count_experiment(
        experiment_image,
        angle_counts,
        detector_count=24
    )

    st.session_state["experiment_results"] = experiment_results


if "experiment_results" in st.session_state:

    results = st.session_state["experiment_results"]

    st.subheader("Experiment Results")

    st.dataframe(results)

    st.subheader("Reconstruction Error vs Matrix Rank")

    fig, ax = plt.subplots(figsize=(9, 5))

    ranks = [item["rank"] for item in results]
    errors = [item["mse"] for item in results]

    ax.plot(ranks, errors, marker="o")

    ax.set_xlabel("Matrix Rank")
    ax.set_ylabel("Mean Squared Error (MSE)")
    ax.set_title("Reconstruction Error vs Matrix Rank")

    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)
