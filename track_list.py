from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('tracks.db')

@app.route('/tracks', methods=['GET'])
def list_tracks():
    # Get every entry
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, artist FROM tracks")
    songs = [{"title": row[0], "artist": row[1]} for row in cursor.fetchall()]

    # Close connection
    conn.close()
    
    # Return 404 instead of an empty list
    if not songs:
        return jsonify({"status": "Not Found"}), 404
    
    # Else return songs
    return jsonify({"songs": songs}), 200


if __name__ == '__main__':
    app.run(debug=True, port=1002)