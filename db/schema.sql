CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT NOT NULL,
    image_height INTEGER NOT NULL,
    image_width INTEGER NOT NULL,
    projection_angles INTEGER NOT NULL,
    detector_count INTEGER NOT NULL,
    matrix_rank INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS phantoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL,
    phantom_type TEXT NOT NULL,
    FOREIGN KEY (scan_id) REFERENCES scans(id)
);

CREATE TABLE IF NOT EXISTS beam_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL,
    projection_angles INTEGER NOT NULL,
    detector_count INTEGER NOT NULL,
    FOREIGN KEY (scan_id) REFERENCES scans(id)
);

CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL,
    measurement_index INTEGER NOT NULL,
    measurement_value REAL NOT NULL,
    FOREIGN KEY (scan_id) REFERENCES scans(id)
);

CREATE TABLE IF NOT EXISTS reconstructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL,
    image_height INTEGER NOT NULL,
    image_width INTEGER NOT NULL,
    reconstruction_data TEXT NOT NULL,
    mse REAL,
    rmse REAL,
    FOREIGN KEY (scan_id) REFERENCES scans(id)
);
