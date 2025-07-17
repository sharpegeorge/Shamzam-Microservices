from flask import Flask, request, jsonify
import sqlite3
import audd_api
import base64

app = Flask(__name__)

def get_db():
    return sqlite3.connect('tracks.db')

@app.route('/trackrequest', methods=['POST'])
def track_request():

    # Get the uploaded audio file from the request
    uploadedAudio = request.get_json()

    # Check if audio file exists
    if 'audio' not in uploadedAudio:
        return jsonify({"status": "Bad Request", "message": "Missing 'audio' file"}), 400

    rawUploadedAudio = uploadedAudio['audio']

    # Use audd.io API to recognise song
    result = audd_api.recognise_audio(rawUploadedAudio)

    # Check for any errors returned by function
    if result.get('status') == 'API request failed':
        return jsonify({"status": "Recognition failed"}), 500

    if result.get('status') == 'No match found':
        return jsonify({"status": "API could not identify song"}), 404

    title, artist = result.values()

    # Find song track in database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT song FROM tracks WHERE title = ? AND artist = ?", (title, artist))
    songs = [{"audio": row[0]} for row in cursor.fetchall()]
    conn.close()

    # Check for no entry of song in database
    if len(songs) == 0:
        return jsonify({"status": "No entry of song in database"}), 404

    # Composite key of 'title' and 'artist' so duplicates can't exist

    # Read song file
    returnAudio = songs[0]

    return returnAudio, 200

if __name__ == '__main__':
    app.run(debug=True, port=1003)