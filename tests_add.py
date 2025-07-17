import unittest
from database import reset_db
import track_add
import base64

class testCase(unittest.TestCase):
    def setUp(self):
        # Reset the database and set up the test client before each test
        self.mock = track_add.app.test_client()
        reset_db()

    def test_post_tracks_success(self):
        """Happy Path - successfully add a new track"""

        # Reading track and encodes to base64 
        with open("wavs/Blinding Lights.wav", "rb") as file:
            uploadAudio = base64.b64encode(file.read()).decode("utf-8")

        payload = {
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "audio": uploadAudio
        }

        # posting song payload
        response = self.mock.post('/tracks', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data.get("status"), "Created")

    def test_post_tracks_missing_field(self):
        """Unhappy Path - missing 'song' field"""

        payload = {"title": "Blinding Lights", "artist": "The Weeknd"}

        # posting song payload with missing audio
        response = self.mock.post('/tracks', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_post_tracks_invalid_audio(self):
        """Unhappy Path - invalid song data format"""

        payload = {"title": "Blinding Lights", "artist": "The Weeknd", "audio": 12345}

        # posting song payload with invalid audio
        response = self.mock.post('/tracks', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_post_tracks_duplicate(self):
        """Unhappy Path - duplicate track entry"""

        # Reading track and encodes to base64 
        with open("wavs/Blinding Lights.wav", "rb") as file:
            uploadAudio = base64.b64encode(file.read()).decode("utf-8")

        payload = {
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "audio": uploadAudio
        }

        # posting song payload twice to get duplicate error
        self.mock.post('/tracks', json=payload)
        response = self.mock.post('/tracks', json=payload)
        self.assertEqual(response.status_code, 409)