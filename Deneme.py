# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 16:23:03 2022

@author: Onur
"""

import investpy
import time
from datetime import date
from pathlib import Path
import os
import yfinance as yf, pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import numpy as np
import ta

path = os.getcwd()+"\Günlük"

data_ta = pd.read_csv(path+"\Avalanche.csv")


mom_data = add_all_ta_features(data_ta, open="Open", high="High", low="Low", close="Close", volume="Volume")


data = pd.read_csv(path+"\Avalanche.csv")
# Datetime conversion
data['Date'] = pd.to_datetime(data.Date)
# Setting the index
data.set_index('Date', inplace=True)

data.drop("Currency",axis=1,inplace=True)

def SMA(df, periods=50):
    """
    Calculating the Simple Moving Average for the past n days
    
    **Values must be descending**
    """
    lst = []
        
    for i in range(len(df)):
        if i < periods:
            
            # Appending NaNs for instances unable to look back on
            lst.append(np.nan)
            
        else:
            # Calculating the SMA
            lst.append(round(np.mean(df[i:periods+i]), 2))
        
    return lst
  
  
  
def Stoch(closes, lows, highs, periods=14, d_periods=3):
    """
    Calculating the Stochastic Oscillator for the past n days
    
    **Values must be descending**
    """
    k_lst = []
    
    d_lst = []
    
    for i in range(len(closes)):
        if i < periods:
            
            # Appending NaNs for instances unable to look back on
            k_lst.append(np.nan)
            
            d_lst.append(np.nan)
            
        else:
            
            # Calculating the Stochastic Oscillator
            
            # Calculating the %K line
            highest = max(highs[i:periods+i])
            lowest = min(lows[i:periods+i])
            
            k = ((closes[i] - lowest) / (highest - lowest)) * 100
            
            k_lst.append(round(k, 2))
            
            # Calculating the %D line
            if len(k_lst) < d_periods:
                d_lst.append(np.nan)
            else:
                d_lst.append(round(np.mean(k_lst[-d_periods-1:-1]).astype(int)))
    
    return k_lst, d_lst
    

def RSI(df, periods=14):
    """
    Calculates the Relative Strength Index
    
    **Values must be descending**
    """
    
    df = df.diff()
    
    lst = []
    
    for i in range(len(df)):
        if i < periods:
            
            # Appending NaNs for instances unable to look back on
            lst.append(np.nan)
            
        else:
            
            # Calculating the Relative Strength Index          
            avg_gain = (sum([x for x in df[i:periods+i] if x >= 0]) / periods)
            avg_loss = (sum([abs(x) for x in df[i:periods+i] if x <= 0]) / periods)


            rs = avg_gain / avg_loss

            rsi = 100 - (100 / (1 + rs))

            lst.append(round(rsi, 2))

            
    return lst

sma = SMA(data)
k_lst, d_lst = Stoch(data.Close,data.Low,data.High)
#rsi = RSI(data)

# TA's RSI
data['ta_rsi'] = ta.momentum.rsi(data.Close)
# TA's Stochastic Oscillator
data['ta_stoch_k'] = ta.momentum.stoch(data.High, data.Low, data.Close)
data['ta_stoch_d'] = ta.momentum.stoch_signal(data.High, data.Low, data.Close)


search_result = investpy.search_quotes(text='Avax', products=['cryptos'], n_results=1)

technical_indicators = search_result.retrieve_technical_indicators(interval="daily")

historical_data = search_result.retrieve_historical_data(from_date="27/03/2022", 
                                                to_date="29/03/2022")

information = search_result.retrieve_information()


"""
technical_indicators = search_result.retrieve_technical_indicators(interval="daily")
print(technical_indicators)
"""