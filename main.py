import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from pathlib import Path
import os

pd.set_option('display.width', None)


files = [file for file in os.listdir('Resources/')]
print(files)


sp500_historical = pd.read_csv('Resources/' + files[4], index_col='Date', parse_dates=True, infer_datetime_format=True).sort_index()

algo_returns = pd.read_csv('Resources/' + files[1], index_col='Date', parse_dates=True, infer_datetime_format=True).sort_index()
whale_returns = pd.read_csv('Resources/' + files[5], index_col='Date', parse_dates=True, infer_datetime_format=True).sort_index()

# Read Whale Returns
print(whale_returns)
print(whale_returns.isna().sum())
whale_returns.dropna(inplace = True)
print(whale_returns.isna().sum())

# Read and clean Algo Returns
print(algo_returns)
print(algo_returns.isna().sum())
algo_returns.dropna(inplace = True)
print(algo_returns.isna().sum())

# Read and clean SP500 historical
print(sp500_historical)
print(sp500_historical.isna().sum())
sp500_historical.dropna(inplace = True)
print(sp500_historical.isna().sum())

print(sp500_historical.head())

## Removing the dollar signs from SP500

sp500_historical= sp500_historical.apply(lambda x: x.str.replace('$','').apply(lambda x: float(x))).dropna()
print(sp500_historical.head())

## Finding the sp500 returns
sp500_returns = sp500_historical.pct_change().dropna()
sp500_returns.columns = ['SP500 Returns']
print(sp500_returns)

# Combine the three return dataframes

combined_return_df = pd.concat([sp500_returns,whale_returns,algo_returns], axis = 'columns',join = 'inner')
print(combined_return_df)

# Plot the daily returns of all the portfolios
# combined_return_df.plot(figsize = (20,10))
# plt.show()

# Calculating and plotting the cumulative returns for each portfolio

combined_cumulative_returns = (1 + combined_return_df).cumprod().plot(figsize = (20,10))
title = plt.title('Cumulative Returns of All Portfolios')
plt.tight_layout()

# plt.show()

# Risk analysis

# Create a boxplot of the portfolios






