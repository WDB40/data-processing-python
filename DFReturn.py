# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 22:29:19 2020

@author: mattq
"""



import pandas as pd
from datetime import date, timedelta
import Ondemand
from Config import api_key, end_point


od = Ondemand.OnDemandClient(api_key, end_point)


Symbol = input("Enter Stock Symbol: ")
Symbol.upper()
daysPast = input("Enter desired previous Days for analysis: ")
while True:
    try:
        daysPast = float(daysPast)
        break
    except ValueError:
        daysPast = input("Please enter desired Days again: ")

def currentData(s):
    
    quotes = od.quote(s)['results']
    df = pd.DataFrame.from_dict(quotes)

    return (df)


def historicData(s, dP):
    today = date.today()
    pDate = today- timedelta(days=dP)
    sDate = date(year = pDate.year, month=pDate.month, day=pDate.day)
    sDate = sDate.strftime("%Y%m%d")
    weekHistory = od.history(s, 'daily', startDate=sDate)['results']
    df = pd.DataFrame.from_dict(weekHistory)

    return (df)


todayDF = currentData(Symbol)
historyDF = historicData(Symbol, daysPast)

