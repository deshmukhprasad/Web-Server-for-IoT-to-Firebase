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
import statsmodels.api as sm 
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

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

freq = 0  #counter for freq

db = firebase.database()

def noquote(s):																			# The function to remove the bug in Pyrebase lib about sort function
    return s
pyrebase.pyrebase.quote = noquote

# timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string

@app.route('/tdata/', methods=['GET'])
def predict():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	air = float(request.args['air'])
	wlev = int(request.args['wlev'])
	hum = int(request.args['hum'])
	wet1 = int(request.args['wet1'])
	wet2 = int(request.args['wet2'])
	temp = int(request.args['temp'])
	soap = int(request.args['soap'])
	tid = request.args['tid']
	#data preprocessing	
	# wlev = abs(50 - wlev)/5
	# hum = abs(hum - 60)/4
	# temp = int(abs(temp -20)/2)

	# prediction for features
	# pm = pickle.load(open('fmodel', 'rb'))
	# predict_fn = lambda x: pm.predict_proba(x).astype(float) 						#predict function for features. lime
	# t = dl.load(open('explainer','rb'))
	# y = pd.DataFrame([[air,wlev,hum,wet,ldr]])
	# yd = y.values																	#loading the pre-trained explorer
	# exp = t.explain_instance(yd[0], predict_fn, num_features=5)						#predicting the features
	
	data = { 'date': timeStamp, 'air': air, 'wlev': wlev, 'hum': hum, 'wet1': wet1, 'wet2': wet2, 'temp': temp }		#data to be pushed
	db.child(tid).child("ctdata").update(data)													# updating real time data
	db.child(tid).child("tdata").child(timeStamp).set(data)									#querrrying database to push the data with timestamp as key
	db.child(tid).child("soap").set(soap)
	return '''<h1>The feature value is: {}</h1>'''.format(data)

@app.route('/freq/', methods=['GET'])
def freq():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	cfreq = int(request.args['cfreq'])
	tid = request.args['tid']		#to receive frequency
	freq = db.child(tid).child("cfreq").get().val()['cfreq']
	if cfreq == 0:
		freq = 0
	elif cfreq == 1:
		freq = freq + 1
	db.child(tid).child("cfreq").update({"cfreq": freq})
	db.child(tid).child("freq").child(timeStamp).set({"date": timeStamp, "freq": freq})
	return '''<h1>The feature value is: {}</h1>'''.format(freq)

@app.route('/feed/', methods=['GET'])
def feed():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	feed = int(request.args['feed'])
	tid = request.args['tid']																					#to receive feed back value
	if feed == 1:																										#To check feed back is clean = 1 or dirty = 0
		clean = db.child(tid).child("feed_stat").child("happy").get()																#To get previous number of clean feedbacks
		for x in clean.each():
			tclean = x.val()
		tclean = int(tclean) + 1																						#Update the number
		db.child(tid).child("feed_stat").child("happy").update({"number": tclean})													#Updating in firebase
	else:
		dirty = db.child(tid).child("feed_stat").child("sad").get()																
		for x in dirty.each():
			tdirty = x.val()
		tdirty = int(tdirty) + 1
		db.child(tid).child("feed_stat").child("sad").update({"number": tdirty})
	db.child(tid).child("feed").child(timeStamp).set({"date": timeStamp, "feed": feed})											#Setting feedback value with timestamp
	return '''<h1>The feature value is: {}</h1>'''.format(feed)

@app.route('/att/', methods=['GET'])
def att():
	timeStamp = datetime.now().astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")						#converting timestamp into string
	att = int(request.args['att'])
	tid = request.args['tid']																						#to receive attendance
	if (att == 1):																										# 1 if cleaner is about to clean
		db.child(tid).child("att").child(timeStamp).set({"date": timeStamp})														# mark the attendance of the cleaner
	elif(att == 0):																										# 0 if cleaner has cleaned the toilet
		date_res = db.child(tid).child("att").order_by_key().limit_to_last(1).get()												#To get the time stamp of attendance
		for date in date_res.each():
			before_date = date.val()

		bdata = db.child(tid).child("tdata").order_by_key().end_at(before_date['date']).limit_to_last(1).get()						# To get the data just before the attendance
		for data in bdata.each():
			bair = data.val()['air']
			bwlev = data.val()['wlev']

		cdata = db.child(tid).child("tdata").order_by_key().limit_to_last(1).get()													# To get the data after the cleaning
		for data in cdata.each():
			cair = data.val()['air']
			cwlev = data.val()['wlev']

		if ((int(bair) - int(cair)) < 0 or (int(bwlev) - int(cwlev)) < 0):												# Comparing of the data
			db.child(tid).child("cqual").child(timeStamp).set({"date": timeStamp, "quality": 0})
		else:
			db.child(tid).child("cqual").child(timeStamp).set({"date": timeStamp, "quality": 1})

	return '''<h1>The feature value is: {}</h1>'''

@app.route('/pred/', methods=['GET'])
def pred():
	tid = request.args['tid']
	temp_results = sm.load('temp_results.pickle')
	air_results = sm.load('air_results.pickle')
	wlev_results = sm.load('wlev_results.pickle')
	hum_results = sm.load('hum_results.pickle')

	y_hat_avg = pd.DataFrame(index=np.arange(24), columns=np.arange(4))

	y_hat_avg[0] = air_results.forecast(24)
	y_hat_avg[1] = wlev_results.forecast(24)
	y_hat_avg[2] = temp_results.forecast(24)
	y_hat_avg[3] = hum_results.forecast(24)

	for x in range(len(y_hat_avg[0])):
		# print(x)
		db.child(tid).child("prediction").child("air").child(x).set({"hour" : x, "val" : "{:.2f}".format(y_hat_avg[0][x])})

	for x in range(len(y_hat_avg[0])):
		# print(x)
		db.child(tid).child("prediction").child("wlev").child(x).set({"hour" : x, "val" : "{:.2f}".format(y_hat_avg[1][x])})

	for x in range(len(y_hat_avg[0])):
		# print(x)
		db.child(tid).child("prediction").child("temp").child(x).set({"hour" : x, "val" : "{:.2f}".format(y_hat_avg[2][x])})

	for x in range(len(y_hat_avg[0])):
		# print(x)
		db.child(tid).child("prediction").child("hum").child(x).set({"hour" : x, "val" : "{:.2f}".format(y_hat_avg[3][x])})

	return '''<h1>The feature value is: </h1>'''

if __name__ == "__main__":
    app.run(debug=True)
