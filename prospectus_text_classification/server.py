import spacy
from flask import Flask, request, jsonify, logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = spacy.load('model/classification')

logger = logging.create_logger(app)
logger.info('Flask logger created.')


def predict_class(text):
    if not text:
        return {}
    return model(text).cats


@app.route('/predict', methods=['GET', 'POST'])
def result():
    data = request.get_json()['input']
    response = jsonify([predict_class(text) for text in data])
    return response


@app.route('/')
def index():
    return 'Prediction server'


app.run(host='0.0.0.0')
