from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('tracks.db')

@app.route('/tracks', methods=['POST'])
def add_track():
    # Get new song data and unpack
    newSong = request.json
    title, artist, audio = newSong.get("title"), newSong.get("artist"), newSong.get("audio")

    # Check all fields exist and the song is a string
    if not title or not artist or not isinstance(audio, str):
        return jsonify({"status": "Bad Request", "message": "Invalid song format"}), 400

    # Open connection to database
    conn = get_db()
    cursor = conn.cursor()

    # Check if track already exists and if so return error
    cursor.execute("SELECT * FROM tracks WHERE title=? AND artist=?", (title, artist))
    if cursor.fetchone():
        conn.close() # close connection to database
        return jsonify({"status": "Conflict - Track already exists"}), 409

    # Insert track into database
    cursor.execute("INSERT INTO tracks (title, artist, song) VALUES (?, ?, ?)", (title, artist, audio))

    # Close connection to database
    conn.commit()
    conn.close()

    return jsonify({"status": "Created"}), 201
    

if __name__ == '__main__':
    app.run(debug=True, port=1000)