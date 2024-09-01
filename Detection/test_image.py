import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the pre-trained model
model_path = r'models\weights\real_fake_model.h5'
loaded_model = load_model(model_path)

# Define the image dimensions for the model input
img_width, img_height = 224, 224

# Function to prepare an image for prediction
def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to detect face in an image
def detect_face(img_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return False, "No face found"

    return True, "Face detected"

# Function to predict if an image is real or fake
def predict_image(img_path):
    face_detected, msg = detect_face(img_path)
    if not face_detected:
        return msg, None

    img_array = prepare_image(img_path)
    prediction = loaded_model.predict(img_array)
    if prediction[0][0] > 0.5:
        return 'Real', prediction[0][0]
    else:
        return 'Fake', 1 - prediction[0][0]

# Specify the path of the image
image_path = r"C:\Users\tomeh\OneDrive\Desktop\receipt1.png"

# Get the prediction
prediction, confidence = predict_image(image_path)
if confidence is not None:
    print(f'Prediction: {prediction}, Confidence: {confidence}')
else:
    print(prediction)
