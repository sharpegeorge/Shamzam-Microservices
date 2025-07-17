import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from database import reset_db
import track_remove

class testCase(unittest.TestCase):
    def setUp(self):
        # Reset the database and set up the test client before each test
        self.mock = track_remove.app.test_client()
        reset_db()

    @patch("track_remove.get_db")
    def test_remove_track_success(self, mock_get_db):
        """Happy Path - successfully removing a track"""
        # Using MagicMock so remove function doesn't affect the mock database
        mock_conn = MagicMock() # mocking connection to database
        mock_get_db.return_value = mock_conn
        
        response = self.mock.delete('/tracks/The Weeknd/Blinding Lights')
        self.assertEqual(response.status_code, 200)

        status = response.get_json()['status']
        self.assertEqual(status, "Deleted")

    @patch("track_remove.get_db")
    def test_delete_track_not_found(self, mock_get_db):
        """Unhappy Path - trying to remove a non-existent track"""
        # Using MagicMock so remove function doesn't affect the mock database
        mock_conn = MagicMock() # mocking connection to database
        mock_get_db.return_value = mock_conn

        mock_cursor = MagicMock() # mocking connection to cursor
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # simulates no track found
        
        response = self.mock.delete('/tracks/Unknown/Unknown')
        self.assertEqual(response.status_code, 404)

    @patch("track_remove.get_db")
    def test_delete_track_bad_format(self, mock_get_db):
        """Unhappy Path - sending url with missing arguments"""
        mock_conn = MagicMock() # mocking connection to database
        mock_get_db.return_value = mock_conn
        
        response = self.mock.delete('/tracks/The Weeknd/')  # No title
        self.assertEqual(response.status_code, 404)

        response = self.mock.delete('/tracks//Blinding Lights')  # No artist
        self.assertEqual(response.status_code, 404)