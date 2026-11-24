
GET_ALL_SCANS = """
SELECT * FROM scans
ORDER BY id DESC;
"""

GET_SCAN_BY_ID = """
SELECT * FROM scans
WHERE id = ?;
"""

DELETE_SCAN = """
DELETE FROM scans
WHERE id = ?;
"""

COUNT_SCANS = """
SELECT COUNT(*) FROM scans;
"""
