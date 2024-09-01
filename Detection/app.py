from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the pre-trained model
model_path = r'models\weights\real_fake_model.h5'
loaded_model = load_model(model_path)

# Define the image dimensions
img_width, img_height = 224, 224

# Function to prepare an image for prediction
def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict if an image is real or fake
def predict_image(img_path):
    img_array = prepare_image(img_path)
    prediction = loaded_model.predict(img_array)
    if prediction[0][0] > 0.5:
        return 'Real', prediction[0][0]
    else:
        return 'Fake', 1 - prediction[0][0]

@app.route('/')
def index():
    return render_template("detection_image.html")

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        prediction, confidence = predict_image(filename)
        image_url = url_for('uploaded_file', filename=file.filename)
        return render_template('detection_image.html', result=prediction, confidence=confidence, image_url=image_url)
    else:
        return jsonify({'error': 'Invalid file type'})

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=5002, debug=True)
