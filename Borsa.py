# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 19:46:00 2022

@author: Onur
"""

import investpy
import time
from datetime import date
from pathlib import Path
import os
import pandas as pd

runtimelist=[]
indexlist=[]
connectionlist=[]
valuelist=[]
path = os.getcwd()+"\Aylık"


def CointoCsv(x='Bitcoin'):
    today = date.today()
    todaysdate = today.strftime("%d/%m/%Y")
    
    """
    data = investpy.get_crypto_recent_data(crypto=x)
    """
    try:
        data = investpy.get_crypto_historical_data(crypto=x, 
                                                   from_date='01/01/1950', 
                                                   to_date=todaysdate, 
                                                   as_json=False, 
                                                   order='ascending', 
                                                   interval='Monthly')
        if "/" in x:
            print("LOOOO: "+x)
            x = x.replace("/"," ")
            print("LOOOO222: "+x)
        """path = os.getcwd()+"\Haftalık" """
        export_path = os.path.join(path, x + '.csv')
        data.to_csv(export_path)
        """data.to_csv(x+'.csv')"""
        time.sleep(3)
    except(IndexError):
        print("IndexError: "+x)
        indexlist.append(x)
        pass  
    except(RuntimeError): 
        print("RuntimeError: "+x)
        runtimelist.append(x)
        time.sleep(500)
        pass
    except(ConnectionAbortedError,ConnectionError): 
        print("ConnectionAbortedError: "+x)
        connectionlist.append(x)
        time.sleep(300)
        pass
    except(ValueError): 
        print("ValueError: "+x)
        valuelist.append(x)
        pass
        
crypto = investpy.get_cryptos()

"""
CointoCsv('Stacks')
"""

for row in range(len(crypto)):   
   CointoCsv(crypto.loc[row,'name'])
   
"""
import glob

Günlük = {}
for filename in glob.glob('C:/Users/Onur/Desktop/Borsa/Günlük/*.csv'):
    Günlük[filename[:-4]] = pd.read_csv(filename, sep="|")
    
Aylık = {}
for filename in glob.glob('C:/Users/Onur/Desktop/Borsa/Aylık/*.csv'):
    Aylık[filename[:-4]] = pd.read_csv(filename, sep="|")
    
Haftalık = {}
for filename in glob.glob('C:/Users/Onur/Desktop/Borsa/Haftalık/*.csv'):
    Haftalık[filename[:-4]] = pd.read_csv(filename, sep="|")
"""