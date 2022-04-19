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


path = os.getcwd()+"\Altın"


def CointoCsv():
    today = date.today()
    todaysdate = today.strftime("%d/%m/%Y")
    
    """
    data = investpy.get_crypto_recent_data(crypto=x)
    """
    data = investpy.get_commodity_historical_data(commodity='gold', 
                                                  country='TURKEY',
                                                  from_date='01/01/1900', 
                                                  to_date=todaysdate)

    export_path = os.path.join(path, 'Gold/TRY' + '.csv')
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
commodities = investpy.commodities.get_commodities_list()
test = investpy.commodities.get_commodities_dict()
test2 = investpy.commodities.get_commodities()


CointoCsv()

