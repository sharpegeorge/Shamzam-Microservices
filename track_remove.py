from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    # Opens connection to database
    return sqlite3.connect('tracks.db')

@app.route('/tracks/<artist>/<title>', methods=['DELETE'])
def delete_track(artist, title):
    # Check both parameters given
    if not title or not artist:
        return jsonify({"status": "Bad Request"}), 400

    # Check song exists in database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks WHERE title=? AND artist=?", (title, artist))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"status": "Not Found"}), 404

    # Removes song from database and closes connection
    cursor.execute("DELETE FROM tracks WHERE title=? AND artist=?", (title, artist))
    conn.commit()
    conn.close()

    return jsonify({"status": "Deleted"}), 200
    

if __name__ == '__main__':
    app.run(debug=True, port=1001)