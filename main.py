import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import os

pd.set_option('display.width', None)


files = [file for file in os.listdir('Resources/')]
print(files)


sp500_historical = pd.read_csv('Resources/' + files[4], index_col='Date', parse_dates=True, infer_datetime_format=True).sort_index()

algo_returns = pd.read_csv('Resources/' + files[1], index_col='Date', parse_dates=True, infer_datetime_format=True).sort_index()
whale_returns = pd.read_csv('Resources/' + files[5], index_col='Date', parse_dates=True, infer_datetime_format=True).sort_index()

# Read and clean Whale Returns
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

# combined_cumulative_returns = (1 + combined_return_df).cumprod().plot(figsize = (20,10))
# title = plt.title('Cumulative Returns of All Portfolios')
# plt.tight_layout()
#
# plt.show()

# Risk analysis

## Create a boxplot of the portfolios
#
# combined_return_df.boxplot(figsize=(20,10), grid = True)
# title = plt.title('Box Plot of the Return of All Portfolios')
# y_label = plt.ylabel('Returns as Percents')
# plt.show()




## Calculating the daily standard deviations of all portfolio returns

combined_daily_std = combined_return_df.std()
sp500_daily_std = combined_daily_std.iloc[1]

print(combined_daily_std)

riskier_portfolios = []
less_risky_portfolio = []
for i in combined_daily_std.index:
    Portfolio = i
    std = combined_daily_std[i]
    SP500 = combined_daily_std[0]
    if std > SP500:
        riskier_portfolios.append([Portfolio])
    elif std == SP500:
        pass
    elif std < SP500:
        less_risky_portfolio.append(Portfolio)

print(f'The following Portfolios are riskier than the SP500: \n\n '
      f'{riskier_portfolios}')
print(f'The following portfolios are less risky than the SP500:\n\n'
      f'{less_risky_portfolio}')

combined_annualized_std = combined_daily_std * np.sqrt(250)
print(combined_annualized_std)

# Rolling statistics

## 21-day rolling standard deviation

# rolling_std_21 = combined_return_df.rolling(window = 21).std()
# rolling_std_21.plot(figsize = (20,10))
# ylabel = plt.ylabel('Standard Deviation')
# title = plt.title('21-Day Rolling Standard Deviation of All Portfolios')
# plt.show()

## Calculating and plotting the correlation of all the portfolios.
# correlation = combined_return_df.corr()
# sns.heatmap(correlation,vmax = -1, vmin = 1, annot = True)
# plt.show()

# Calculate and plot Beta for each portfolio.

## Finding each portfolio
soros_fund = whale_returns.iloc[:,0]
paulson_fund = whale_returns.iloc[:,1]
tiger_fund = whale_returns.iloc[:,2]
berkshire_fund = whale_returns.iloc[:,3]


## Finding the variance and covariance and beta.
sp500_variance = sp500_returns['SP500 Returns'].var()

algo1_beta = algo_returns['Algo 1'].cov(sp500_returns['SP500 Returns']) / sp500_variance
algo2_beta = algo_returns['Algo 2'].cov(sp500_returns['SP500 Returns']) / sp500_variance
soros_beta = soros_fund.cov(sp500_returns['SP500 Returns']) / sp500_variance
paulson_beta = paulson_fund.cov(sp500_returns['SP500 Returns']) / sp500_variance
tiger_beta = tiger_fund.cov(sp500_returns['SP500 Returns']) / sp500_variance
berkshire_beta = berkshire_fund.cov(sp500_returns['SP500 Returns']) / sp500_variance

## Finding the 21-day rolling average beta for soros_fund

soros_rolling_covar  = soros_fund.rolling(window = 21).cov(sp500_returns['SP500 Returns'])
rolling_var = sp500_returns['SP500 Returns'].rolling(window = 21).var()

soros_rolling_beta = (soros_rolling_covar / rolling_var).dropna()

# soros_rolling_beta.plot()
# plt.show()

# Rolling Beta with EWM
# soros_rolling_covar  = soros_fund.ewm(halflife= '21 days', times = soros_fund.index).cov(sp500_returns['SP500 Returns'])
# rolling_var = sp500_returns['SP500 Returns'].rolling(window = 21).var()


#Exponentially Weighted Average of the returns of Soros's Fund.
soros_ewm_returns= soros_fund.ewm(halflife='21 days', times = soros_fund.index).mean()
#
# a.plot()
# plt.show()