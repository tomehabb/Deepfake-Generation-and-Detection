from flask import Flask, render_template, request, jsonify, send_from_directory
from models.generation.image_2_image import face_swap as image_face_swap
from models.generation.image_2_video import face_swap as video_face_swap
import cv2
import base64
import numpy as np
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("face_swap.html")

@app.route('/video_swap')
def video_swap():
    return render_template("video_swap.html")

@app.route('/swap', methods=['POST'])
def swap_faces():
    # Get the images from the request
    original_image = request.files['original']
    target_image = request.files['target']

    # Convert the images to OpenCV format
    original_image = cv2.imdecode(np.frombuffer(original_image.read(), np.uint8), cv2.IMREAD_COLOR)
    target_image = cv2.imdecode(np.frombuffer(target_image.read(), np.uint8), cv2.IMREAD_COLOR)

    # Perform the face swap
    swapped_image = image_face_swap(original_image, target_image)

    # Convert the swapped image to base64
    _, buffer = cv2.imencode('.jpg', swapped_image)
    swapped_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Return the swapped image
    return jsonify({'swapped_image': swapped_image_base64})

@app.route('/swap_video', methods=['POST'])
def swap_faces_video():
    # Get the image and video from the request
    original_image = request.files['original']
    target_video = request.files['target']

    # Save the uploaded files temporarily
    original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_original_image.jpg')
    target_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_target_video.mp4')
    output_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_video.mp4')

    original_image.save(original_image_path)
    target_video.save(target_video_path)

    # Perform the face swap
    final_output_path = video_face_swap(original_image_path, target_video_path, output_video_path)

    # Run detection after swapping
    run_script(
        script_path=r"D:/Projects/Deepfake Generation and Detection/Detection/app.py",
        python_executable=r"C:/Users/tomeh/miniconda3/envs/detect_1/python.exe"
    )

    # Clean up temporary files
    os.remove(original_image_path)
    os.remove(target_video_path)

    # Return the path to the swapped video
    return jsonify({'swapped_video': f'/videos/{os.path.basename(final_output_path)}'})

# New route to serve the uploaded video
@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def run_script(script_path, python_executable):
    # Command to activate the conda environment and run the script in PowerShell
    command = f'powershell.exe -Command "& {{ {python_executable} {script_path} }}"'
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{script_path} completed successfully.")
    else:
        print(f"{script_path} failed with error: {result.stderr}")
    
    return result.returncode

if __name__ == '__main__':
    app.run(port=5001, debug=True)
