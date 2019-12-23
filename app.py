import numpy as np
from sklearn.linear_model import LogisticRegression
import dill as dl
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import lime
import lime.lime_tabular
import pyrebase

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyC3BCU_3v_kFnQp-lt60vvrU5fYlJnIm4Q",
    "authDomain": "feedback-beb57.firebaseapp.com",
    "databaseURL": "https://feedback-beb57.firebaseio.com",
    "projectId": "feedback-beb57",
    "storageBucket": "feedback-beb57.appspot.com",
    "messagingSenderId": "211570371404",
    "appId": "1:211570371404:web:f781b483e59e428bc4fde9"
  	}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

@app.route('/', methods=['GET'])
def predict():
	air = int(request.args['air'])
	wlev = int(request.args['wlev'])
	hum = int(request.args['hum'])
	wet = int(request.args['wet'])
	ldr = int(request.args['ldr'])
	feed = int(request.args['feed'])

	# prediction for features
	pm = pickle.load(open('fmodel', 'rb'))
	predict_fn = lambda x: pm.predict_proba(x).astype(float) 						#predict function for features. lime
	t = dl.load(open('explainer','rb'))
	y = pd.DataFrame([[air,wlev,hum,wet,ldr]])
	yd = y.values																	#loading the pre-trained explorer
	exp = t.explain_instance(yd[0], predict_fn, num_features=5)						#predicting the features
	db.child("a1").push(exp.as_list())


	return '''<h1>The feature value is: {}</h1>'''.format(exp.as_list())

if __name__ == "__main__":
    app.run(debug=True)
