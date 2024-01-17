import requests
import pandas as pd
import numpy as np
from math import floor
from termcolor import colored as cl
import matplotlib.pyplot as plt
from get_historical_data import *
from plot import *
from implement import *
from plot_macd import *
from calculate_macd import *

if __name__ == "__main__":

    position = []
    for i in range(len(macd_signal)):
        if macd_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)

    for i in range(len(ibm['close'])):
        if macd_signal[i] == 1:
            position[i] = 1
        elif macd_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]

    macd = ibm_macd['macd']
    signal = ibm_macd['signal']
    close_price = ibm['close']
    macd_signal = pd.DataFrame(macd_signal).rename(
        columns={0: 'macd_signal'}).set_index(ibm.index)
    position = pd.DataFrame(position).rename(
        columns={0: 'macd_position'}).set_index(ibm.index)

    frames = [close_price, macd, signal, macd_signal, position]
    strategy = pd.concat(frames, join='inner', axis=1)

    strategy

    ibm_ret = pd.DataFrame(np.diff(ibm['close'])).rename(
        columns={0: 'returns'})
    macd_strategy_ret = []

    for i in range(len(ibm_ret)):
        try:
            returns = ibm_ret['returns'][i]*strategy['macd_position'][i]
            macd_strategy_ret.append(returns)
        except:
            pass

    macd_strategy_ret_df = pd.DataFrame(
        macd_strategy_ret).rename(columns={0: 'macd_returns'})

    investment_value = 100000
    number_of_stocks = floor(investment_value/ibm['close'][0])
    macd_investment_ret = []

    for i in range(len(macd_strategy_ret_df['macd_returns'])):
        returns = number_of_stocks*macd_strategy_ret_df['macd_returns'][i]
        macd_investment_ret.append(returns)

    macd_investment_ret_df = pd.DataFrame(
        macd_investment_ret).rename(columns={0: 'investment_returns'})
    total_investment_ret = round(
        sum(macd_investment_ret_df['investment_returns']), 2)
    profit_percentage = floor((total_investment_ret/investment_value)*100)
    print(cl('Profit gained from the MACD strategy by investing $100k in IBM : {}'.format(
        total_investment_ret), attrs=['bold']))
    print(cl('Profit percentage of the MACD strategy : {}%'.format(
        profit_percentage), attrs=['bold']))
