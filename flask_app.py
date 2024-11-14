from flask import Flask, render_template, send_from_directory, request
import os
import urllib.parse

app = Flask(__name__, template_folder='.')

# Helper function to find the correct case-insensitive path
def find_file(directory, filename):
    # Check all files in the directory for a case-insensitive match
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Compare with the filename decoded (handling spaces as %20 etc.)
            if file.lower() == filename.lower().replace('%20', ' '):
                return os.path.join(root, file)
    return None

# Route for the main selection page
@app.route('/')
def selection_page():
    return render_template('SelectionPage.html')

# Route for the game board (index.html)
@app.route('/index')
def game_board():
    return render_template('index.html')

# Route for level 3
@app.route('/level3')
def level3():
    return render_template('level3.html')

# Route to serve audio files case-insensitively
@app.route('/level3/audio/<path:filename>')
def serve_audio(filename):
    # Decode the filename to handle spaces and special characters
    decoded_filename = urllib.parse.unquote(filename)
    audio_path = find_file('level3/audio', decoded_filename)
    if audio_path:
        return send_from_directory(os.path.dirname(audio_path), os.path.basename(audio_path))
    return "File not found", 404

# Route to serve the listening_sen.txt file case-insensitively
@app.route('/level3/listening_sen.txt')
def serve_text():
    return send_from_directory('level3', 'listening_sen.txt')

if __name__ == '__main__':
    app.run(debug=True)
