import pandas as pd
import numpy as np
from model.encode import train_encode_library
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

def predict_function(sample, model):
    print("running")
    # IMPORTANT: USE THE SUITABLE ORIENT
    test = pd.DataFrame.from_dict(sample, orient='index')
    # if you have any step of data transformation, include it here
    test_encoded = test.replace(train_encode_library, inplace=False)
    # predict
    y_pred = model.predict(test_encoded)
    return y_pred

def evaluate_function(sample, model):

    # IMPORTANT: USE THE SUITABLE ORIENT
    test = pd.DataFrame.from_dict(sample, orient='index')

    # separate features / label column here:
    X_test = test.iloc[:, :-1]
    y_test = test['income_>50K']
    print(X_test)

    # label encoder
    X_test_encoded = X_test.replace(train_encode_library, inplace=False)

    # predict
    y_pred = model.predict(X_test_encoded)

    # evaluate
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')

    return accuracy, precision
