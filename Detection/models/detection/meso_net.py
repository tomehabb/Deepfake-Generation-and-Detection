import os
import cv2
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Dropout, LeakyReLU
from keras.optimizers import Adam

image_dimensions = {'height': 256, 'width': 256, 'channels': 3}

class Classifier:
    def __init__(self):
        self.model = None
    
    def predict(self, x):
        return self.model.predict(x)
    
    def fit(self, x, y):
        return self.model.train_on_batch(x, y)
    
    def get_accuracy(self, x, y):
        return self.model.test_on_batch(x, y)
    
    def load(self, path):
        self.model.load_weights(path)

class Meso4(Classifier):
    def __init__(self, learning_rate=0.001):
        super().__init__()
        self.model = self.init_model()
        optimizer = Adam(learning_rate=learning_rate)  # Use 'learning_rate' instead of 'lr'
        self.model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])
    
    def init_model(self): 
        x = Input(shape=(image_dimensions['height'], image_dimensions['width'], image_dimensions['channels']))
        
        x1 = Conv2D(8, (3, 3), padding='same', activation='relu')(x)
        x1 = BatchNormalization()(x1)
        x1 = MaxPooling2D(pool_size=(2, 2), padding='same')(x1)
        
        x2 = Conv2D(8, (5, 5), padding='same', activation='relu')(x1)
        x2 = BatchNormalization()(x2)
        x2 = MaxPooling2D(pool_size=(2, 2), padding='same')(x2)
        
        x3 = Conv2D(16, (5, 5), padding='same', activation='relu')(x2)
        x3 = BatchNormalization()(x3)
        x3 = MaxPooling2D(pool_size=(2, 2), padding='same')(x3)
        
        x4 = Conv2D(16, (5, 5), padding='same', activation='relu')(x3)
        x4 = BatchNormalization()(x4)
        x4 = MaxPooling2D(pool_size=(4, 4), padding='same')(x4)
        
        y = Flatten()(x4)
        y = Dropout(0.5)(y)
        y = Dense(16)(y)
        y = LeakyReLU(alpha=0.1)(y)
        y = Dropout(0.5)(y)
        y = Dense(1, activation='sigmoid')(y)

        return Model(inputs=x, outputs=y)

def predict_fake_frames(input_path, output_folder, model):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    deepfake_detected = False  # Flag to track if deepfaked frames are detected

    if os.path.isfile(input_path):
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Single image
            frame = cv2.imread(input_path)
            if frame is not None:
                frame = cv2.resize(frame, (256, 256))
                normalized_frame = frame.astype('float32') / 255.0
                input_frame = np.expand_dims(normalized_frame, axis=0)
                prediction = model.predict(input_frame)
                if prediction <= 0.8:
                    cv2.imwrite(f'{output_folder}/frame_{os.path.basename(input_path)}.jpg', frame)
                    deepfake_detected = True
        elif input_path.lower().endswith(('.mp4', '.avi', '.mkv')):
            # Video file
            cap = cv2.VideoCapture(input_path)
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1
                resized_frame = cv2.resize(frame, (256, 256))
                normalized_frame = resized_frame.astype('float32') / 255.0
                input_frame = np.expand_dims(normalized_frame, axis=0)
                prediction = model.predict(input_frame)
                if prediction <= 0.7:
                    cv2.imwrite(f'{output_folder}/frame_{frame_count}.jpg', frame)
                    deepfake_detected = True
            cap.release()

    return deepfake_detected  # Return True if deepfaked frames are detected and saved, otherwise False

meso = Meso4()
meso.load(r'models\weights\real_fake_model.h5')  # Use raw string for the path
