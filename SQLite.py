# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:38:45 2022

@author: Onur
"""

import sqlite3
import pandas as pd
import glob
import os
from pathlib import Path

path = os.getcwd()+"\ParaBirimleri"

conn = sqlite3.connect('Para.db')
c = conn.cursor()

def CSVtoSQL(x):
    path='C:/Users/Onur/Desktop/Borsa/ParaBirimleri/'+x
    data = pd.read_csv(path)
    x = x.split(".")
    print(x[0])
    data.to_sql(x[0], conn, if_exists='append', index = False)
    
coin_list = {}
for file in os.listdir(path):
    hold = coin_list.get(file[:12],[])
    hold.append(file)
    coin_list[file[:12]] = hold

coin_pairs = []
for game, stats in coin_list.items():
    coin_pairs.append(stats)

coin_pairs = pd.DataFrame(coin_pairs)
coin_pairs.columns =['Name']

for row in range(len(coin_pairs)):   
    CSVtoSQL(coin_pairs.loc[row,'Name'])
    



"""
data.to_sql('users', conn, if_exists='append', index = False)


data.to_sql(x, conn, if_exists='append', index = False)
"""