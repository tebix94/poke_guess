import os
from tensorflow.keras.models import load_model
import numpy as np
from numpy.typing import NDArray
from PIL import Image

def predict_image(prediction_dict):
    # Load image and resize it
    img = Image.open(prediction_dict['path'])
    img = img.resize((400, 400))
    # Convert image to NumPy array
    img_array = np.array(img)
    img_array = img_array[:, :, :3] # Remove the 4th channel (alpha channel)
    img_array = img_array / 255.
    img_array = np.expand_dims(img_array, axis=0)
    # Close image
    img.close()
    # Load CNN model
    model = load_model('./pokeguess.keras')
    # Predict image
    score = model.predict(img_array)
    # Load labels
    img_labels = np.load('./img_labels.npy')
    # Get unique class names from the labels
    class_names = np.unique(img_labels).tolist()
    # Get results
    if np.max(score) < 0.5:
        prediction_name = 'Unknown'
        prediction_confidence = f'N/A'
    else:
        prediction_name = class_names[np.argmax(score)]
        prediction_confidence = f'{100 * np.max(score):.2f}'
    # Update prediction dictionary
    prediction_dict['name'] = prediction_name
    prediction_dict['confidence'] = prediction_confidence
    # Print results for testing purposes only
    print(f'Predicted: {class_names[np.argmax(score)]} ({100 * np.max(score):.2f}%)')