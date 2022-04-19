# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:49:47 2022

@author: Onur
"""

import investpy
import time
from datetime import date
from pathlib import Path
import os


technical_indicators = investpy.search_result.retrieve_technical_indicators(interval="daily")
print(technical_indicators)

path = os.getcwd()+"\İndikatörs"


def CointoCsv():
    today = date.today()
    todaysdate = today.strftime("%d/%m/%Y")
    
    """
    data = investpy.get_crypto_recent_data(crypto=x)
    """
    data = investpy.technical_indicators(name='Bitcoin', country='turkey', product_type='coin', interval='daily')
    
    export_path = os.path.join(path, 'İndikatörs' + '.csv')
    data.to_csv(export_path)
"""
    try:
        data = investpy.get_commodity_historical_data(commodity='gold', 
                                                      country='TRY',
                                                      from_date='01/01/1900', 
                                                      to_date=todaysdate)

        export_path = os.path.join(path, 'Gold/TRY' + '.csv')
        data.to_csv(export_path)
    except(IndexError):
        print("IndexError:")
        pass  
    except(RuntimeError): 
        print("RuntimeError:")
        pass
    except(ConnectionAbortedError,ConnectionError): 
        print("ConnectionAbortedError: ")
        pass
    except(ValueError): 
        print("ValueError: ")
        pass
 """      



CointoCsv()

