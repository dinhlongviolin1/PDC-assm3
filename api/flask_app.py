import os
import pickle
from numpy.core.arrayprint import repr_format
import pandas as pd
import json
from flask import Flask, jsonify, request
import numpy as np
from flask_controller import predict_function, evaluate_function
from dash_app import createDash

MODEL_PATH = "pickle_model.pkl"
with open(MODEL_PATH, "rb") as rf:
    model = pickle.load(rf)

# Init the app
server = Flask(__name__)

#Integrate Dash into Flask
dashApp = createDash(server, '/dashboard/')



# App health check
@server.route("/", methods=["GET"])
def healthcheck():
    msg = (
        "The server is running"
    )
    return jsonify({"message": msg})

# Predict route
@server.route("/predict", methods=["POST"])
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
@server.route("/evaluate", methods=["POST"])
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

#Dashboard
@server.route('/dashboard')
def myDashApp():
    return dashApp.index()

# main
# if __name__ == '__main__':
#     server.run(debug=True)
