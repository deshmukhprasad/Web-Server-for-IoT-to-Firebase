import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.api as sm 
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

new_results = sm.load('longley_results.pickle')

# df = pd.read_csv('data.csv')
# df.Timestamp = pd.to_datetime(df.datetime)
# df.index = df.Timestamp

# train = df[0:432]
# train.Timestamp = pd.to_datetime(train.datetime)

# test = df[432:]
# test.Timestamp = pd.to_datetime(test.datetime)

# df = df.resample('60min').mean()
# train = train.resample('60min').mean()
# test = test.resample('60min').mean()

#y_hat_avg = test.copy()

y_hat_avg = pd.DataFrame(index=np.arange(12), columns=np.arange(1))

print(y_hat_avg.shape)

y_hat_avg[0] = new_results.forecast(12)

print(y_hat_avg)



# train.Air.plot(figsize=(15,8), title = 'Air Quality', fontsize= 14)
# test.Air.plot(figsize=(15,8), title = 'Air Quality', fontsize= 14)
# y_hat_avg.Holt_linear.plot(figsize=(15,8), title = 'Air Quality', fontsize= 14)
# plt.show()