import json
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "ct_scans.db"


def get_connection():
    """Create a connection to the SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the scans table if it does not exist."""

    schema_path = Path(__file__).resolve().parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    with get_connection() as connection:
        connection.executescript(schema)



def save_scan(
    image_name,
    image_height,
    image_width,
    projection_angles,
    detector_count,
    matrix_rank,
    phantom_type=None,
    measurements=None,
    reconstructed_image=None,
    mse=None,
    rmse=None
):
    """Save scan details and related reconstruction data."""

    if not image_name or not image_name.strip():
        raise ValueError("Image name cannot be empty.")

    values = [
        image_height,
        image_width,
        projection_angles,
        detector_count,
        matrix_rank
    ]

    if any(
        not isinstance(value, int)
        or isinstance(value, bool)
        for value in values
    ):
        raise ValueError("Scan measurements must be integers.")

    if image_height <= 0 or image_width <= 0:
        raise ValueError("Image dimensions must be positive.")

    if projection_angles <= 0 or detector_count <= 0:
        raise ValueError("Angles and detectors must be positive.")

    if matrix_rank < 0:
        raise ValueError("Matrix rank cannot be negative.")

    with get_connection() as connection:

        # Save main scan record
        cursor = connection.execute(
            """
            INSERT INTO scans (
                image_name,
                image_height,
                image_width,
                projection_angles,
                detector_count,
                matrix_rank
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                image_name.strip(),
                image_height,
                image_width,
                projection_angles,
                detector_count,
                matrix_rank
            )
        )

        scan_id = cursor.lastrowid

        # Save phantom information
        if phantom_type is not None:
            connection.execute(
                """
                INSERT INTO phantoms (scan_id, phantom_type)
                VALUES (?, ?)
                """,
                (scan_id, phantom_type)
            )

        # Save beam configuration
        connection.execute(
            """
            INSERT INTO beam_configs (
                scan_id,
                projection_angles,
                detector_count
            )
            VALUES (?, ?, ?)
            """,
            (scan_id, projection_angles, detector_count)
        )

        # Save individual measurements
        if measurements is not None:
            measurement_values = (
                measurements.tolist()
                if hasattr(measurements, "tolist")
                else list(measurements)
            )

            connection.executemany(
                """
                INSERT INTO measurements (
                    scan_id,
                    measurement_index,
                    measurement_value
                )
                VALUES (?, ?, ?)
                """,
                [
                    (scan_id, index, float(value))
                    for index, value in enumerate(measurement_values)
                ]
            )

        # Save reconstructed image and quality metrics
        if reconstructed_image is not None:
            reconstruction_data = json.dumps(
                reconstructed_image.tolist()
                if hasattr(reconstructed_image, "tolist")
                else reconstructed_image
            )

            connection.execute(
                """
                INSERT INTO reconstructions (
                    scan_id,
                    image_height,
                    image_width,
                    reconstruction_data,
                    mse,
                    rmse
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    scan_id,
                    image_height,
                    image_width,
                    reconstruction_data,
                    mse,
                    rmse
                )
            )

        return scan_id

    """Save a scan record into the database."""

    if not image_name or not image_name.strip():
        raise ValueError("Image name cannot be empty.")

    values = [
        image_height,
        image_width,
        projection_angles,
        detector_count,
        matrix_rank
    ]

    if any(
        not isinstance(value, int)
        or isinstance(value, bool)
        for value in values
    ):
        raise ValueError("Scan measurements must be integers.")

    if image_height <= 0 or image_width <= 0:
        raise ValueError("Image dimensions must be positive.")

    if projection_angles <= 0 or detector_count <= 0:
        raise ValueError("Angles and detectors must be positive.")

    if matrix_rank < 0:
        raise ValueError("Matrix rank cannot be negative.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO scans (
                image_name,
                image_height,
                image_width,
                projection_angles,
                detector_count,
                matrix_rank
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                image_name.strip(),
                image_height,
                image_width,
                projection_angles,
                detector_count,
                matrix_rank
            )
        )

        return cursor.lastrowid


def get_all_scans():
    """Retrieve all saved scan records."""

    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM scans ORDER BY id DESC"
        )

        return [dict(row) for row in cursor.fetchall()]


def get_scan_by_id(scan_id):
    """Retrieve one scan using its ID."""

    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM scans WHERE id = ?",
            (scan_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None


def delete_scan(scan_id):
    """Delete a scan record using its ID."""

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM scans WHERE id = ?",
            (scan_id,)
        )

        return cursor.rowcount > 0
