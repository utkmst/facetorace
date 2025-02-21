from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

# Load the model
model = load_model('second_model.pkl')

# Define the race categories
race_categories = ['East Asian', 'Indian', 'Black', 'White', 'Middle Eastern', 'Latino_Hispanic', 'Southeast Asian']

@app.route('/predict', methods=['POST'])
def predict():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No selected files'}), 400

    results = []
    for file in files:
        try:
            img = Image.open(file.stream).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            predictions = model.predict(img_array)
            predicted_race = race_categories[np.argmax(predictions)]
            
            results.append({'predicted_race': predicted_race})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)