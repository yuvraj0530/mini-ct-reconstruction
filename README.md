# Mini CT Scan Reconstruction Using Linear Algebra

## 1. Project Overview

Mini CT Scan Reconstruction is an educational 2D Computed Tomography (CT) simulation project developed using Python and Linear Algebra.

The project demonstrates how an image can be reconstructed from multiple projection measurements using matrix operations and the least-squares method.

It also demonstrates how measurement noise affects reconstruction quality.

## 2. Objectives

- Understand the mathematical principles behind CT reconstruction.
- Generate a beam matrix using linear algebra.
- Simulate projection measurements.
- Reconstruct images using least-squares approximation.
- Analyze matrix rank, nullity and solution uniqueness.
- Study the effect of measurement noise.
- Store scan records using SQLite.
- Visualize results through an interactive dashboard.
 
## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| NumPy | Matrix operations and numerical computation |
| Matplotlib | Data visualization |
| Streamlit | Interactive web interface |
| SQLite | Scan history database |
| SciPy | Optional numerical validation |
| Pytest | Unit testing |

## 4. Project Features

1. **Phantom Generation:** Generate square, circular and custom test images.
2. **Beam Matrix Generation:** Construct the mathematical system matrix representing beam paths through image pixels.
3. **Measurement Simulation:** Generate projection measurements from the original image.
4. **Image Reconstruction:** Reconstruct images using NumPy's least-squares solver.
5. **Matrix Analysis:** Calculate rank, nullity, independent measurements and system type.
6. **Matrix Operations:** Perform transpose, multiplication, determinant and inverse operations.
7. **Noise Simulation:** Add Gaussian noise to projection measurements.
8. **Reconstruction Quality:** Calculate MSE, RMSE and relative error.
9. **Measurement Comparison:** Visualize clean and noisy measurements.
10. **Database Integration:** Store and retrieve scan history using SQLite.
11. **Scan Queue:** Manage scan requests using a FIFO queue.

## 5. Mathematical Background

The CT reconstruction problem is represented as:

\[
Ax=b
\]

Where:

- A = Beam matrix
- x = Unknown image pixel values
- b = Projection measurements

The reconstructed image is calculated using the least-squares method:

\[
x^*=\underset{x}{\operatorname{argmin}}\|Ax-b\|_2^2
\]

The project also uses matrix rank and nullity to study whether a unique solution is possible.

## 6. Reconstruction Quality Metrics

**Mean Squared Error (MSE)**

Measures the average squared difference between the original and reconstructed images.

**Root Mean Squared Error (RMSE)**

Represents the square root of MSE.

**Relative Error**

Measures reconstruction error relative to the norm of the original image.

## 7. Installation and Execution

### Step 1: Clone or download the project

Open the project directory in VS Code.

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
python -m streamlit run app/interface.py
```

The application will open in your browser.

## 8. Running Tests

Execute the following command from the project root:

```bash
python -m pytest -v
```

**Current test status:** 52 tests passed.

## 9. Experimental Results

The project demonstrates how increasing measurement noise affects reconstruction quality.

| Noise Level | MSE | RMSE | Relative Error |
|---|---:|---:|---:|
| 0% | 0.026987 | 0.164277 | 0.328553 |
| 5% | 0.081520 | 0.285518 | 0.571036 |
| 10% | 0.271789 | 0.521334 | 1.042668 |

These are observed results from the current experimental configuration. The reconstruction metrics can vary with the scan configuration and random noise realization.

## 10. Limitations

- This is a simplified 2D educational simulation.
- It does not represent a clinical CT scanner.
- The reconstruction model uses simplified parallel-beam projections.
- Reconstruction quality depends on projection angles, detector count and measurement noise.
- It is not intended for medical diagnosis.

## 11. Conclusion

The project demonstrates the practical application of Linear Algebra in Computed Tomography image reconstruction.

It combines matrix operations, least-squares approximation, rank analysis, data structures, database management and visualization into one interactive Python application.

It also demonstrates the relationship between measurement noise and reconstruction accuracy.

## 12. Future Scope

- Implement additional reconstruction algorithms.
- Improve reconstruction quality for underdetermined systems.
- Add more phantom images.
- Explore different projection geometries.
- Improve the visualization and experimental analysis.

---

**Project:** Mini CT Scan Reconstruction Using Linear Algebra  
**Application:** Educational 2D CT Simulator