from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/')
def home():
    return render_template('PhotoUpload.html')

@app.route('/Upload-Image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result = subprocess.run(
            ['python', 'fatsecret.py'],
            check=True,
            capture_output=True,
            text=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Notebook'}), 500

    return jsonify({'message': 'Image received', 'filename': filename, 'output': output})

@app.route('/Results')
def results():
    return render_template('Results.html')

if __name__ == '__main__':
    app.run(debug=True)