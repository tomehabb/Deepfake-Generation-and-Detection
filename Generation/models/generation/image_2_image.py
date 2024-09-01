import insightface
from insightface.app import FaceAnalysis

# Initialize the FaceAnalysis model
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))

# Initialize the face swapper model
swapper = insightface.model_zoo.get_model('models\weights\inswapper_128.onnx', download=False,
                                          download_zip=False)


def face_swap(source_img, target_img):
    # Detect faces in both images
    source_faces = app.get(source_img)
    target_faces = app.get(target_img)

    # Select the first face in each image
    source_face = source_faces[0]
    target_face = target_faces[0]

    # Perform face swapping
    swapped_img = target_img.copy()
    for face in target_faces:
        swapped_img = swapper.get(swapped_img, face, source_face, paste_back=True)

    return swapped_img
