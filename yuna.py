from flask import Flask, request, jsonify, abort
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import requests

# Tensorflow -------------------------------------------------------------------
tf.enable_eager_execution()
model = None
MODEL_PATH = './static/model.h5'

def emptyModel():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(256, 256, 3)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def classify(model, imgPath):
    # model.fit(norm_images, labels, epochs=5)
    tensor = tf.image.decode_image(tf.io.read_file(imgPath))
    tensor = tf.image.resize(tensor, [256, 256])
    tensor /= 255.0
    tensor = np.expand_dims(tensor, 0)
    predictions = model.predict(tensor)
    return np.argmax(predictions[0])

def downloadFile(url):
    dst = './static/' + url.split('/')[-1]
    req = requests.get(url)
    if (req.status_code != 200):
        return None
    with open(dst, 'wb') as f:
        f.write(req.content)
    return dst

# Flask ------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'yuna',
        'tensorflow': tf.__version__,
        'ready': model is not None
    }), 200

@app.route('/load', methods=['GET'])
def load():
    global model
    if (not os.path.isfile(MODEL_PATH)):
        model = emptyModel()
        return jsonify({'msg': 'Created empty model'}), 200
    model = keras.models.load_model(MODEL_PATH)
    return jsonify({'msg': 'Loaded model from file'}), 200

@app.route('/save', methods=['GET'])
def save():
    if (model is None):
        abort(403)
    model.save(MODEL_PATH)
    return jsonify({'msg': 'Saved model to file'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if (not request.json or not 'url' in request.json):
        abort(400)
    if (model is None):
        abort(403)
    imgPath = downloadFile(request.json['url'])
    if (imgPath is None):
        abort(502)
    res = classify(model, imgPath)
    return jsonify({'prediction': res}), 200
