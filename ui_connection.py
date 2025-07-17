from flask import Flask, request, jsonify, url_for
from agent import smart_home_agent
from speak_to_text import speak_to_text
from text_to_speak import text_to_speech
import os
app = Flask(__name__)

@app.route('/')
def index():
    return open("templates/ui.html").read()

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    command = data.get('command', '')
    print(command)
    result = smart_home_agent(command)
    return jsonify({"message": result})

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        audio_file = request.files.get('voice')

        if not audio_file or audio_file.filename == '':
            return jsonify({'reply': 'No audio file received.'}), 400

        text = speak_to_text(audio_file)

        print("text: " + text)
        if not text:
            return jsonify({'reply': 'Could not extract text from audio.'}), 400

        file_path = "static/audio/response.wav"
        if os.path.exists(file_path):
            os.remove(file_path)

        result = smart_home_agent(text)
        text_to_speech(result)

        return jsonify({"reply": result})
    except Exception as e:
        print("Error in process_audio:", e)
        return jsonify({'reply': 'Internal server error during audio processing.'}), 500
@app.route('/get-audio')
def get_audio():
    audio_url = url_for('static', filename='audio/response.wav')
    print(audio_url)
    try:
        return jsonify({'audio_url': audio_url})
    except:

        print("Error in get_audio")


app.run(debug=True,host='0.0.0.0', port=5000)