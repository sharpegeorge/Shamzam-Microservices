import unittest
from ../database import reset_db
import ../track_list
from unittest.mock import patch
import sqlite3

class testCase(unittest.TestCase):
    def setUp(self):
        # Reset the database and set up the test client before each test
        self.mock = track_list.app.test_client()
        reset_db()

    @patch("track_list.get_db")
    def test_list(self, mock_get_db):
        """Happy Path - retrieve tracks when database has entries"""
        mock_get_db.return_value = sqlite3.connect('../mock_database.db') # using mock database for testing

        # getting data from database
        response = self.mock.get('/tracks')
        songs = response.get_json()['songs']
        firstSongName = songs[0]['title']
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(songs), 2)
        self.assertEqual(firstSongName, 'Blinding Lights')

    def test_get_tracks_empty(self):
        """Unhappy Path - retrieve tracks when database is empty"""
        response = self.mock.get('/tracks')
        self.assertEqual(response.status_code, 404)  # 404 indicates empty db