# -*- coding: utf-8 -*-
"""ARIMA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n1GxwYbXPRntPsJx-4lrz1TzbzVg0Ykh
"""

# Import libraries

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# Read the csv file into a dataframe
data = pd.read_csv("household_power_consumption.txt", sep=';')

# Replace '?' characters with NaN values to process the data as numbers later
data['Global_active_power'] = data['Global_active_power'].replace('?', np.nan)
data['Sub_metering_1'] = data['Sub_metering_1'].replace('?', np.nan)
data['Sub_metering_2'] = data['Sub_metering_2'].replace('?', np.nan)
data['Sub_metering_3'] = data['Sub_metering_3'].replace('?', np.nan)

# Calculate Active Power
data['Active_Power'] = pd.to_numeric(data['Global_active_power']) * 1000/60 - pd.to_numeric(data['Sub_metering_1']) - pd.to_numeric(data['Sub_metering_2']) - pd.to_numeric(data['Sub_metering_3'])

# Splitting data into train and test sets
train_size = int(len(data) * 0.8)
train, test = data.iloc[:train_size], data.iloc[train_size:]

# Train the ARIMA model
model = ARIMA(train['Active_Power'], order=(1,1,0))
model_fit = model.fit()

num_steps = len(test)

# Forecasting
forecast_results = model_fit.forecast(steps=num_steps)

# Create a DataFrame with forecasted values and a simple integer index
forecast_df = pd.DataFrame({'Active_Power': forecast_results})

# Calculate RMSE
rmse = np.sqrt(np.mean((test['Active_Power'] - forecast_df['Active_Power'])**2))
print("Root Mean Squared Error (RMSE):", rmse)

forecast_results

print("Length of test set:", len(test))
print("Length of forecasted series:", len(forecast_df))