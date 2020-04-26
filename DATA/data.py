import pandas as pd
from datetime import datetime
import numpy as np

date_rng = pd.date_range(start='1/1/2018', periods=576, freq='5T')
print(len(date_rng))
df = pd.DataFrame(date_rng, columns=['Time'])
df['air'] = np.concatenate((np.random.randint(1,5,size=(72)), np.random.randint(4,10,size=(72)), np.random.randint(3,8,size=(72)), np.random.randint(4,10,size=(72)), np.random.randint(1,5,size=(72)), np.random.randint(4,10,size=(72)), np.random.randint(3,8,size=(72)), np.random.randint(4,10,size=(72))), axis = None)

df['wlev'] = np.concatenate((np.random.randint(10,11,size=(72)), np.random.randint(7,10,size=(72)), np.random.randint(4,7,size=(72)), np.random.randint(4,7,size=(72)), np.random.randint(10,11,size=(72)), np.random.randint(7,10,size=(72)), np.random.randint(4,7,size=(72)), np.random.randint(4,7,size=(72))), axis = None)

df['hum'] = np.concatenate((np.random.randint(1,5,size=(72)), np.random.randint(4,10,size=(72)), np.random.randint(3,8,size=(72)), np.random.randint(4,10,size=(72)), np.random.randint(1,5,size=(72)), np.random.randint(4,10,size=(72)), np.random.randint(3,8,size=(72)), np.random.randint(4,10,size=(72))), axis = None)

df['wet1'] = np.concatenate((np.random.randint(0,1,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,1,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72))), axis = None)

df['wet2'] = np.concatenate((np.random.randint(0,1,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,1,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72)), np.random.randint(0,2,size=(72))), axis = None)

df['temp'] = np.concatenate((np.random.randint(30,32,size=(72)), np.random.randint(30,34,size=(72)), np.random.randint(33,37,size=(72)), np.random.randint(33,37,size=(72)), np.random.randint(30,32,size=(72)), np.random.randint(30,34,size=(72)), np.random.randint(32,37,size=(72)), np.random.randint(33,37,size=(72))), axis = None)


df['datetime'] = pd.to_datetime(df['Time'])

df = df.set_index('datetime')
df.drop(['Time'], axis=1, inplace=True)
print(df.head())

df.to_csv('data.csv')