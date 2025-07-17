import unittest
from ../database import reset_db
import base64
import ../track_request
from unittest.mock import patch
import sqlite3

class testCase(unittest.TestCase):
    def setUp(self):
        # Reset the database and set up the test client before each test
        self.mock = track_request.app.test_client()
        reset_db()

    @patch("track_request.get_db")
    def test_trackrequest_success(self, mock_get_db):
        """Happy Path - successfully identify a track from audio data"""

        mock_get_db.return_value = sqlite3.connect('mock_database.db') # using mock database for testing

        # Reading track fragment and encodes to base64 
        with open("../wavs/~Blinding Lights.wav", "rb") as file:
            uploadAudio = {"audio": base64.b64encode(file.read()).decode("utf-8")}

        # Posts request
        response = self.mock.post('/trackrequest', json=uploadAudio)
        self.assertEqual(response.status_code, 200) 

        # Getting correct audio track
        with open("../wavs/Blinding Lights.wav", "rb") as file:
            correctAudio = base64.b64encode(file.read()).decode("utf-8")

        # Getting audio track from response
        returnedAudio = response.get_json()['audio']

        self.assertEqual(correctAudio, returnedAudio)

    @patch("track_request.get_db")
    def test_trackrequest_unknown_song(self, mock_get_db):
        """Unhappy Path - request song not found in database"""

        mock_get_db.return_value = sqlite3.connect('mock_database.db') # using mock database for testing

        # Reading track fragment of a song not registered in mock database
        with open("../wavs/~Don't Look Back In Anger.wav", "rb") as file:
            uploadAudio = {"audio": base64.b64encode(file.read()).decode("utf-8")}

        response = self.mock.post('/trackrequest', json=uploadAudio)
        self.assertEqual(response.status_code, 404)

    @patch("track_request.get_db")
    def test_trackrequest_not_song(self, mock_get_db):
        """Unhappy Path - sending an audio file which is not a song"""

        mock_get_db.return_value = sqlite3.connect('mock_database.db') # using mock database for testing

        # Reading track fragment of a speech and not a song
        with open("../wavs/~Davos.wav", "rb") as file:
            uploadAudio = {"audio": base64.b64encode(file.read()).decode("utf-8")}

        response = self.mock.post('/trackrequest', json=uploadAudio)
        self.assertEqual(response.status_code, 404)

    def test_trackrequest_missing_audio(self):
        """Unhappy Path - missing 'audio' field"""

        # posting empty audio
        uploadAudio = {}
        response = self.mock.post('/trackrequest', json=uploadAudio)
        self.assertEqual(response.status_code, 400)
