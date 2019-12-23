from __future__ import print_function
import pandas as pd 
import numpy as np 
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
#import seaborn as sns
import pandas as pd
import dill as dl
import lime
import lime.lime_tabular
import pickle



data = pd.read_csv('Book1.csv', usecols = ['Air','water', 'Humidity', 'Wet', 'Feedback', 'Health'])

X = data[['Air','water', 'Humidity', 'Wet', 'Feedback']]
y = data['Health']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

lr = LogisticRegression()
lr.fit(X_train,y_train)
pickle.dump(lr, open('fmodel', 'wb'))

# print(lr.predict(X_test))

# score = lr.score(X_test, y_test)
# print(score)

Xtrain = X_train.values

pm = pickle.load(open('fmodel', 'rb'))

predict_fn = lambda x: pm.predict_proba(x).astype(float)

# explainer = lime.lime_tabular.LimeTabularExplainer(Xtrain ,feature_names = ['Air','water', 'Humidity', 'Wet', 'Feedback'], class_names= ['Healthy', 'Unhealthy'], categorical_features= [4], categorical_names= ['Wet'], kernel_width= 2)
print(Xtrain[1])
# dl.dump(explainer, open('explainer','wb'))
y = pd.DataFrame([[4,8,3,0,5]])
print(y)
yd = y.values
print(yd)
t = dl.load(open('explainer','rb'))
exp = t.explain_instance(yd[0], predict_fn, num_features=5)
print(exp.as_list())