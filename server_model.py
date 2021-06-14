from io import BytesIO
from skimage import transform
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import joblib
import random
model = None


def load_model():
    model = joblib.load(r'E:\JetBrains\demo_env_learn\model_save\cnn_face_4.pkl')
    print("Model loaded")
    return model


def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    from skimage import io,transform
    #image = transform.resize(image,(100,100,3))
    image = np.array(image.resize((100, 100)))[..., :3]
    image = image / 255.0
    image = image.astype('float16')
    image = image.reshape(1,100,100,3)
    # from sklearn.preprocessing import LabelEncoder
    # label_encoder = LabelEncoder()
    # label_encoder.inverse_transform([pred.])
    predict = model.predict(image)
    predict = np.argmax(predict)
    return predict



def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image