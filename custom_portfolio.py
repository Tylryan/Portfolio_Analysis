import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import os

axp_df = pd.read_csv('Custom_Portfolio/AXP.csv', index_col='Date', parse_dates=True, infer_datetime_format=True)
chgg_df = pd.read_csv('Custom_Portfolio/CHGG.csv', index_col='Date', parse_dates=True, infer_datetime_format=True)
ea_df = pd.read_csv('Custom_Portfolio/EA.csv', index_col='Date', parse_dates=True, infer_datetime_format=True)
spy_df = pd.read_csv('Custom_Portfolio/SPY.csv', index_col='Date', parse_dates=True, infer_datetime_format=True)


combined_df = pd.concat([axp_df, chgg_df,ea_df,spy_df], axis = 'columns', join = 'inner').sort_index()
combined_df.columns = ['AXP','CHGG','EA','SPY']
# print(combined_df.head())

#! Calculating the daily returns of all portfolios
combined_daily_returns = combined_df.pct_change().dropna()
print(combined_daily_returns.head())

#! Finding the weighted average assuming you invested equally in all three stocks

weights = [0.25,0.25,0.25,0.25]
print(weights)

weighted_portfolio = combined_daily_returns.dot(weights)
weighted_portfolio.columns = ['Portfolio Weighted Return']
print(weighted_portfolio)

combined_daily_returns['Portfolio Weighted Returns'] = weighted_portfolio
nan_check = combined_daily_returns.isna().sum()
print(combined_daily_returns.head())
#* Calculate the annualized standard deviation of all the columns
#! See if your your portfolio is more or less risky compared to the individual stocks.

combined_df_standard_deviation = combined_daily_returns.std() * np.sqrt(252)
print(combined_df_standard_deviation)

riskier_stock = []
less_risky_stock = []
for i in combined_df_standard_deviation.index:
    stock = i
    std = combined_df_standard_deviation[i]
    portfolio_std = combined_df_standard_deviation[4]
    if std > portfolio_std:
        riskier_stock.append([i,combined_df_standard_deviation[i]])
    elif std < portfolio_std:
        less_risky_stock.append([i,combined_df_standard_deviation[i]])

print(f'The following stocks have more risk than the combined portfolio \n\n'
      f'{riskier_stock} \n\n')

print(f'The following stocks have less risk than the combined portfolio \n\n'
      f'{less_risky_stock}')