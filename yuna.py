from flask import Flask
import tensorflow as tf;

app = Flask(__name__)
tf.enable_eager_execution();

@app.route("/")
def index():
    return tf.__version__
