import requests
import pandas as pd
import numpy as np
from math import floor
from termcolor import colored as cl
import matplotlib.pyplot as plt
from plot import *
from implement import *
from calculate_macd import *


def get_historical_data(start_date=None):
    api_key = 'P4J61NBNP1J3YF3O'
    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&outputsize=full&apikey=demo'

    raw_df = requests.get(api_url).json()

    df = pd.DataFrame(raw_df[f'Time Series (Daily)']).T
    df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low',
                   '4. close': 'close', '5. adjusted close': 'adj close', '6. volume': 'volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[:: -1].drop(['7. dividend amount',
                              '8. split coefficient'], axis=1)
    if start_date:
        df = df[df.index >= start_date]
    return df
