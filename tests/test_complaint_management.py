import unittest
from unittest.mock import patch

from db import get_complaint_history, remove_complaint


class DummyCursor:
    def __init__(self, rows=None, dictionary=False):
        self.rows = rows or []
        self.dictionary = dictionary
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def close(self):
        return None


class DummyConnection:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.commit_calls = 0

    def cursor(self, dictionary=False):
        self.cursor_obj.dictionary = dictionary
        return self.cursor_obj

    def commit(self):
        self.commit_calls += 1

    def close(self):
        return None


class ComplaintManagementTests(unittest.TestCase):
    def test_remove_complaint_marks_record_removed(self):
        cursor = DummyCursor()
        conn = DummyConnection(cursor)

        with patch("db.get_connection", return_value=conn):
            success, message = remove_complaint(12, "Admin")

        self.assertTrue(success)
        self.assertIn("removed", message.lower())
        self.assertEqual(conn.commit_calls, 1)

    def test_get_complaint_history_returns_history_rows(self):
        rows = [{"id": 2, "description": "Old issue", "status": "Removed"}]
        cursor = DummyCursor(rows=rows, dictionary=True)
        conn = DummyConnection(cursor)

        with patch("db.get_connection", return_value=conn):
            history = get_complaint_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["status"], "Removed")


if __name__ == "__main__":
    unittest.main()
