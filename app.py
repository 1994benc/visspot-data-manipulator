import os
import flask
from flask import Flask, request, jsonify, abort
from admin import firebase_admin, db, story_ref, dataset_ref, chart_ref
from auth_required import auth_required, get_user_id
from apikey_required import apikey_required
from core_functions.parse_dataset import parse_dataset
from flask_cors import CORS
import numpy as np
import simplejson
import pandas as pd
from sklearn.linear_model import LinearRegression


app = Flask(__name__)
CORS(app, resources={
     r"/api/*": {"origins": ["https://visspot.com", "https://www.visspot.com"]}})

@app.route('/api')
@auth_required
def home():
    return "You are authorized to access restricted resources"

# Open to the public, but only accessible from the visspot.com
@app.route('/api/reg/predict', methods=['POST'])
@apikey_required
def reg_predict():
    try:
        x = np.array(request.json["x"])
        y = np.array(request.json["y"])
        x_to_predict = np.array(request.json['x_to_predict'])
        reg = LinearRegression().fit(x, y)
        preds = reg.predict(x_to_predict)
        response = jsonify({"predictions": preds.tolist(
        ), "coef": reg.coef_.tolist(), "intercept": reg.intercept_.tolist()})
        return response
    except Exception as e:
        print(e)
        abort(500, description=e)


# For dataset owners only
@app.route("/api/datasets/parse", methods=['GET'])
@apikey_required
def dataset_parse():
    try:
        dataset_id = request.args.get('dataset_id', None)
        if (not dataset_id):
            return jsonify({"dataset_id": None, "message": "Required parameter dataset_id is missing (i.e. ...?dataset_id=<datasetId>)"})
        pagination = request.args.get("pagination", 1)
        page = request.args.get("page", 1)
        page_size = request.args.get("page_size", 42)

        # This function will throw an error if 
        # the dataset is not public and user is not the owner of the dataset
        parsed_dataset_obj = parse_dataset(
            dataset_id, page=int(page), pagination=int(pagination), page_size=int(page_size))

        parsed_datasets = parsed_dataset_obj["data"]
        total_size = parsed_dataset_obj["total_size"]
        response = jsonify(simplejson.dumps(
            {"dataset_id": dataset_id, "dataset": parsed_datasets, "total_size": int(total_size)}, ignore_nan=True))
        return response

    except Exception as e:
        abort(500, description=e)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
