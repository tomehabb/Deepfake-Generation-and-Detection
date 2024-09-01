import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import time
import os
from tqdm import tqdm
import onnxruntime as rt
from moviepy.editor import VideoFileClip, AudioFileClip

def face_swap(source_img_path, target_video_path, output_video_path):
    # Check CUDA availability
    if not rt.get_device() == 'GPU':
        raise Exception("CUDA is not available. Please check your CUDA installation.")

    # Initialize the FaceAnalysis model
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))

    # Initialize the face swapper model
    swapper = insightface.model_zoo.get_model('models/weights/inswapper_128.onnx', download=False, download_zip=False)

    # Load the source image
    source_img = cv2.imread(source_img_path)
    if source_img is None:
        raise ValueError("Source image not found or unable to load.")

    # Extract audio from the original video using moviepy
    video = VideoFileClip(target_video_path)
    audio_path = os.path.join(os.path.dirname(output_video_path), 'original_audio.aac')
    video.audio.write_audiofile(audio_path, codec='aac')

    # Open the video file
    cap = cv2.VideoCapture(target_video_path)

    # Get the video's width, height, and frames per second (fps)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a VideoWriter object to write the output video using MPEG-4 codec
    temp_output_video_path = os.path.join(os.path.dirname(output_video_path), 'temp_output_video.mp4')
    out = cv2.VideoWriter(temp_output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Process each frame
    frame_count = 0
    start_time = time.time()

    # Initialize tqdm progress bar
    pbar = tqdm(total=total_frames, unit='frame')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces in both images
        source_faces = app.get(source_img)
        target_faces = app.get(frame)

        # If no faces are detected in either image, return the original target image
        if len(source_faces) == 0 or len(target_faces) == 0:
            swapped_frame = frame
        else:
            # Select the first face in each image
            source_face = source_faces[0]
            target_face = target_faces[0]

            # Perform face swapping
            swapped_frame = frame.copy()
            for face in target_faces:
                swapped_frame = swapper.get(swapped_frame, face, source_face, paste_back=True)

        # Write the swapped frame to the output video
        out.write(swapped_frame)

        # Update progress bar
        pbar.update(1)
        frame_count += 1

    # Close the progress bar
    pbar.close()

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

    # Combine the processed video (MP4) with the original audio using moviepy
    audio_clip = AudioFileClip(audio_path)
    combined_video = VideoFileClip(temp_output_video_path).set_audio(audio_clip)
    combined_video.write_videofile(output_video_path, codec='libx264', fps=fps)

    # Close the video and audio clips to release the resources
    video.close()
    combined_video.close()
    audio_clip.close()

    # Check if the combined video was created
    if not os.path.exists(output_video_path):
        print(f"Error: Combined video not found at {output_video_path}")
        return None

    # Print the paths and check the current working directory
    print(f"Temp Output Video Path: {temp_output_video_path}")
    print(f"Combined Video Path: {output_video_path}")
    print(f"Current Working Directory: {os.getcwd()}")

    # Remove temporary files
    try:
        os.remove(audio_path)
        os.remove(temp_output_video_path)
    except PermissionError as e:
        print(f"Error removing temporary files: {e}")

    return output_video_path
