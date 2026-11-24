
import pytest

from db import database


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    """Use a separate temporary database for each test."""

    test_db = tmp_path / "test_scans.db"
    schema_path = (
        database.Path(__file__).resolve().parents[1]
        / "db"
        / "schema.sql"
    )

    monkeypatch.setattr(database, "DATABASE_PATH", test_db)

    database.initialize_database()

    return database


def test_database_initialization(temporary_database):
    scans = temporary_database.get_all_scans()

    assert scans == []


def test_save_scan(temporary_database):
    scan_id = temporary_database.save_scan(
        "Test Phantom", 4, 4, 6, 5, 12
    )

    assert scan_id == 1


def test_get_all_scans(temporary_database):
    temporary_database.save_scan(
        "Phantom A", 4, 4, 6, 5, 12
    )

    temporary_database.save_scan(
        "Phantom B", 8, 8, 12, 9, 30
    )

    scans = temporary_database.get_all_scans()

    assert len(scans) == 2
    assert scans[0]["image_name"] == "Phantom B"


def test_get_scan_by_id(temporary_database):
    scan_id = temporary_database.save_scan(
        "Test Phantom", 4, 4, 6, 5, 12
    )

    scan = temporary_database.get_scan_by_id(scan_id)

    assert scan["image_name"] == "Test Phantom"


def test_get_nonexistent_scan(temporary_database):
    scan = temporary_database.get_scan_by_id(999)

    assert scan is None


def test_delete_scan(temporary_database):
    scan_id = temporary_database.save_scan(
        "Test Phantom", 4, 4, 6, 5, 12
    )

    result = temporary_database.delete_scan(scan_id)

    assert result is True
    assert temporary_database.get_scan_by_id(scan_id) is None


def test_delete_nonexistent_scan(temporary_database):
    result = temporary_database.delete_scan(999)

    assert result is False


def test_save_invalid_image_name(temporary_database):
    with pytest.raises(ValueError):
        temporary_database.save_scan(
            "", 4, 4, 6, 5, 12
        )


def test_save_invalid_dimensions(temporary_database):
    with pytest.raises(ValueError):
        temporary_database.save_scan(
            "Test Phantom", 0, 4, 6, 5, 12
        )


def test_save_invalid_rank(temporary_database):
    with pytest.raises(ValueError):
        temporary_database.save_scan(
            "Test Phantom", 4, 4, 6, 5, -1
        )
