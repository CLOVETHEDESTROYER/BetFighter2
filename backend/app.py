# I put everything here in app.py instead of individual endpoint files. app.py is the default file for a flask app.
from flask import Flask, request, jsonify
# https://flask-cors.readthedocs.io/en/latest/#using-json-with-cors
from flask_cors import CORS, cross_origin
from mkTemplateGPT import Winner
import cv2
import numpy as np
import os
import json

app = Flask(__name__)
CORS(app, support_credentials=True)



@app.route('/')
@cross_origin(supports_credentials=True)  #could use this for specific routes but dont need it if you use line 7 above.
def winner():
    print('in this route')
    data = {'Winner': ["Member1", "Member2", "Member3", "CacaBallZ", "nalga", "assmane"]}
    return jsonify(data)


@app.route('/testroute')
def testroute():
    # You can make all of your routes here so they dont have to be in separate files. 
    print('inside open bet')
    data = {'Testing': ["testtest", "testtest2"]}
    return jsonify(data)

@app.route('/mk')
def winner():
    # You can make all of your routes here so they dont have to be in separate files. 
    print('inside open bet')
    data = Winner()
    return jsonify(json.loads(data))

@app.route('/mk2', methods=['POST'])
def mk():
    # Receive the image data from the frontend
    data = request.json

    # Here, you can process the image using OpenCV

    # Return the result as JSON
    result = ({"winner": "No Winner"})
    return jsonify(result)



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)