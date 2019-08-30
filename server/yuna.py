from flask import Flask, jsonify, abort, redirect
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

@app.route('/', methods=['GET'])
def index():
    return redirect('/static/index.html')

@app.route('/api', methods=['GET'])
def api():
    return jsonify({
        'service': 'yuna',
        'tensorflow': tf.__version__
    }), 200

@app.route('/api/detect', methods=['POST'])
def detect():
    if (not request.json or not 'url' in request.json):
        abort(400)
    imgPath = downloadFile(request.json['url'])
    if (imgPath is None):
        abort(502)
    res = recognize(context, imgPath)
    return jsonify(res[imgPath]), 200
