from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
import json

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

    return jsonify({'message': 'Image received', 'filename': filename})

@app.route('/Results')
def display_food():
    with open('output.txt', 'r') as f:
        content = f.read().strip()

    entries = content.split('--------------------------')
    data = []

    for entry in entries:
        lines = entry.strip().split('\n')
        if len(lines) < 5:
            continue

        food_name = lines[0].replace('Food: ', '').strip()
        calories = lines[1].replace('Calories: ', '').replace(' kcal', '').strip()
        fat = lines[2].replace('Fat: ', '').replace(' g', '').strip()
        carbs = lines[3].replace('Carbs: ', '').replace(' g', '').strip()
        protein = lines[4].replace('Protein: ', '').replace(' g', '').strip()

        data.append({
            'name': food_name,
            'calories': calories,
            'fat': fat,
            'carbs': carbs,
            'protein': protein
        })
    
    return render_template('Results.html', data=data)

@app.route('/test')
def test():
    food = [
        {'name': 'Garlic', 'calories': 149, 'fat': 0.5, 'carbs': 33.06, 'protein': 6.36},
        {'name': 'Onion', 'calories': 40, 'fat': 0.1, 'carbs': 9.3, 'protein': 1.1}
    ]
    return render_template('Results.html', food=food)
if __name__ == '__main__':
    app.run(debug=True)