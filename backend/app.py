import os
import sys
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add project root to Python path so ml_model imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_model.whisper_mood_pipeline import process_audio_file

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    _, ext = os.path.splitext(audio_file.filename)
    if ext.lower() != ".wav":
        return jsonify({"error": "Only WAV audio files are supported. Please upload a .wav file."}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_input:
        temp_input.write(audio_file.read())
        temp_path = temp_input.name

    try:
        result = process_audio_file(temp_path)
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
