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


path = os.getcwd()+"\ParaBirimleri"


def CointoCsv():
    today = date.today()
    todaysdate = today.strftime("%d/%m/%Y")
    
    """
    data = investpy.get_crypto_recent_data(crypto=x)
    """
    try:
        data = investpy.get_currency_cross_historical_data(currency_cross='EUR/USD', 
                                                           from_date='01/01/1900',
                                                           to_date=todaysdate)
        
        export_path = os.path.join(path, 'EuroUSD' + '.csv')
        data.to_csv(export_path)
        time.sleep(3)
    except(IndexError):
        print("IndexError:")
        pass  
    except(RuntimeError): 
        print("RuntimeError:")
        time.sleep(500)
        pass
    except(ConnectionAbortedError,ConnectionError): 
        print("ConnectionAbortedError: ")
        time.sleep(300)
        pass
    except(ValueError): 
        print("ValueError: ")
        pass
        
money = investpy.currency_crosses.get_available_currencies()


CointoCsv()

