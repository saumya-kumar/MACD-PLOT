
import requests
import pandas as pd
import numpy as np
from math import floor
from termcolor import colored as cl
import matplotlib.pyplot as plt
from get_historical_data import *
from plot import *
from implement import *
from calculate_macd import *


ibm = get_historical_data('2020-01-01')
ibm_macd = get_macd(ibm['close'], 26, 12, 9)
plot_macd(ibm['close'], ibm_macd['macd'], ibm_macd['signal'], ibm_macd['hist'])

buy_price, sell_price, macd_signal = implement_macd_strategy(
    ibm['close'], ibm_macd)
ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

ax1.plot(ibm['close'], color='skyblue', linewidth=2, label='IBM')
ax1.plot(ibm.index, buy_price, marker='^', color='green',
         markersize=10, label='BUY SIGNAL', linewidth=0)
ax1.plot(ibm.index, sell_price, marker='v', color='r',
         markersize=10, label='SELL SIGNAL', linewidth=0)
ax1.legend()
ax1.set_title('IBM MACD SIGNALS')
ax2.plot(ibm_macd['macd'], color='grey', linewidth=1.5, label='MACD')
ax2.plot(ibm_macd['signal'], color='skyblue', linewidth=1.5, label='SIGNAL')

for i in range(len(ibm_macd)):
    if str(ibm_macd['hist'][i])[0] == '-':
        ax2.bar(ibm_macd.index[i], ibm_macd['hist'][i], color='#ef5350')
    else:
        ax2.bar(ibm_macd.index[i], ibm_macd['hist'][i], color='#26a69a')

plt.legend(loc='lower right')
plt.show()
