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

print(spy_df)