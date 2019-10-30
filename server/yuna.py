from flask import Flask, jsonify, abort, redirect, request
import requests
import tensorflow as tf
import re
import uuid
from afd.afdetector import make_context, recognize

# Setup -------------------------------------------------------------------
context = make_context()

def downloadFile(url):
    dst = f'static/{str(uuid.uuid4())}.{url.split('.')[-1]}'
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException as e:
        return None
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
    url = request.json['url']
    if not bool(re.search('^(jpe?g|png|gif|bmp)$', url.split('.')[-1].lower())):
        abort(400)
    imgPath = downloadFile(url)
    if (imgPath is None):
        abort(502)
    res = recognize(context, imgPath)
    return jsonify(res), 200
