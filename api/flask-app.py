import os
import pickle
from numpy.core.arrayprint import repr_format
import pandas as pd
import json
from flask import Flask, jsonify, request
import numpy as np
from flask_controller import predict_function, evaluate_function

MODEL_PATH = "../model/pickle_model.pkl"
with open(MODEL_PATH, "rb") as rf:
    model = pickle.load(rf)

# Init the app
app = Flask(__name__)

# App health check
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    msg = (
        "This is a sentence to check if the server is running"
    )
    return jsonify({"message": msg})

# Predict route
@app.route("/predict", methods=["POST"])
def predict():
    is_json = request.args.get('is_json')
    sample = request.get_json()
    predictions = predict_function(sample, model)
    if is_json == '1':
        y_final = pd.DataFrame(data=predictions[0:],
                               index=[str(i)
                                      for i in range(predictions.shape[0])],
                               columns=["income_>50K"])
        predictions = json.loads(y_final.to_json(orient='index'))
    else:
        predictions = predictions.tolist()
    result = {
        'prediction': predictions
    }
    return jsonify(result)

# Evaluate router
@app.route("/evaluate", methods=["POST"])
def evaluate():
    sample = request.get_json()
    accuracy, precision, report, cm = evaluate_function(sample, model)
    result = {
        'accuracy': accuracy,
        'precision': precision,
        'report': report,
        'confusion_matrix': cm.tolist()
    }
    return jsonify(result)

# main
if __name__ == '__main__':
    app.run(debug=True)
