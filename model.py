import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.api as sm 
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

df = pd.read_csv('data.csv')
df.Timestamp = pd.to_datetime(df.datetime)
df.index = df.Timestamp

train = df[0:432]
train.Timestamp = pd.to_datetime(train.datetime)

test = df[432:]
test.Timestamp = pd.to_datetime(test.datetime)


df = df.resample('60min').mean()
train = train.resample('60min').mean()
test = test.resample('60min').mean()

y_hat_avg = test.copy()

fit_air = Holt(np.asarray(train["air"])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
fit_wlev = Holt(np.asarray(train["wlev"])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
fit_hum = Holt(np.asarray(train["hum"])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
fit_temp = Holt(np.asarray(train["temp"])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)


fit_air.save("air_results.pickle")
fit_wlev.save("wlev_results.pickle")
fit_hum.save("hum_results.pickle")
fit_temp.save("temp_results.pickle")


y_hat_avg['air'] = fit_air.forecast(len(test))
y_hat_avg['wlev'] = fit_wlev.forecast(len(test))
y_hat_avg['hum'] = fit_hum.forecast(len(test))
y_hat_avg['temp'] = fit_temp.forecast(len(test))

train.air.plot(figsize=(15,8), title = 'Air Quality', fontsize= 14)
test.air.plot(figsize=(15,8), title = 'Air Quality', fontsize= 14)
y_hat_avg.hum.plot(figsize=(15,8), title = 'Air Quality', fontsize= 14)
plt.show()