import numpy as np
from sklearn.linear_model import LogisticRegression
import dill as dl
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import lime
import lime.lime_tabular
import pyrebase
from datetime import datetime
from pytz import timezone

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

# timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string

@app.route('/tdata/', methods=['GET'])
def predict():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	air = int(request.args['air'])
	wlev = int(request.args['wlev'])
	hum = int(request.args['hum'])
	wet1 = int(request.args['wet1'])
	wet2 = int(request.args['wet2'])
	temp = int(request.args['temp'])
	
	#data preprocessing	
	air = int(abs(air )/30)
	wlev = abs(50 - wlev)/5
	hum = abs(hum - 60)/4
	temp = int(abs(temp -20)/2)

	# prediction for features
	# pm = pickle.load(open('fmodel', 'rb'))
	# predict_fn = lambda x: pm.predict_proba(x).astype(float) 						#predict function for features. lime
	# t = dl.load(open('explainer','rb'))
	# y = pd.DataFrame([[air,wlev,hum,wet,ldr]])
	# yd = y.values																	#loading the pre-trained explorer
	# exp = t.explain_instance(yd[0], predict_fn, num_features=5)						#predicting the features
	
	data = { 'date': timeStamp, 'air': air, 'wlev': wlev, 'hum': hum, 'wet1': wet1, 'wet2': wet2, 'temp': temp }		#data to be pushed
	db.child("ctdata").update(data)													# updating real time data
	db.child("tdata").child(timeStamp).set(data)									#querrrying database to push the data with timestamp as key

	return '''<h1>The feature value is: {}</h1>'''.format(data)

@app.route('/freq/', methods=['GET'])
def freq():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	cfreq = int(request.args['cfreq'])				#to receive frequency
	db.child("cfreq").update({"cfreq": cfreq})
	db.child("freq").child(timeStamp).set({"date": timeStamp, "freq": cfreq})
	return '''<h1>The feature value is: {}</h1>'''.format(cfreq)

@app.route('/feed/', methods=['GET'])
def feed():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	feed = int(request.args['feed'])				#to receive feed back
	db.child("freed").child(timeStamp).set({"date": timeStamp, "feed": feed})
	return '''<h1>The feature value is: {}</h1>'''.format(feed)

@app.route('/att/', methods=['GET'])
def att():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	att = int(request.args['att'])				#to receive feed back
	if (att == 1):
		db.child("att").child(timeStamp).set({"date": timeStamp})
	# elif(att == 0):
	# 	pass
		


if __name__ == "__main__":
    app.run(debug=True)