from flask import Flask, jsonify, abort
import requests
import tensorflow as tf
from afdetector import make_context, recognize

# Setup -------------------------------------------------------------------
context = make_context()

def downloadFile(url):
    dst = 'static/' + url.split('/')[-1]
    req = requests.get(url)
    if (req.status_code != 200):
        return None
    with open(dst, 'wb') as f:
        f.write(req.content)
    return dst

# Routes ------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def index():
    return jsonify({
        'service': 'yuna',
        'tensorflow': tf.__version__
    }), 200

@app.route('/api/detect', methods=['GET'])
def predict():
    # if (not request.json or not 'url' in request.json):
        # abort(400)
    # imgPath = downloadFile(request.json['url'])
    imgPath = downloadFile('https://pbs.twimg.com/media/EC-F0pFVUAAumMJ.jpg')
    if (imgPath is None):
        abort(502)
    res = recognize(context, imgPath)
    return jsonify(res[imgPath]), 200
