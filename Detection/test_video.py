import os
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

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

# Directory paths
real_dir = os.path.join(os.getcwd(),r'D:\Projects\Deepfake Generation and Detection\archive\Dataset\Validation\Real')
output_dir = os.path.join(os.getcwd(), r'C:\Users\tomeh\OneDrive\Desktop\Test Images\Detection\Real')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process images and move detected reals
real_count = 0
for img_name in os.listdir(real_dir):
    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(real_dir, img_name)
        prediction, confidence = predict_image(img_path)
        if prediction == 'Real':
            shutil.move(img_path, os.path.join(output_dir, img_name))
            real_count += 1
        if real_count >= 100:
            break

print(f'{real_count} real images moved to {output_dir}')
