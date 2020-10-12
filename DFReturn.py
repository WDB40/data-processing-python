# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 22:29:19 2020

@author: mattq
"""


import Ondemand
import pandas as pd
from datetime import date

today = date.today()

weekAgo = date(year = today.year, month=today.month, day=today.day-7)
weekDate = weekAgo.strftime("%Y%m%d")

symbol = input("Enter Stock Symbol: ")


od = Ondemand.OnDemandClient(api_key='837a2c6b0793be83405c5cb5da6d0c49', end_point='https://marketdata.websol.barchart.com/')

# get quote data for Apple and Microsoft#
quotes = od.quote(symbol)['results']
todayDF = pd.DataFrame.from_dict(quotes)


weekHistory = od.history(symbol, 'daily', startDate=weekDate)['results']

historyDF = pd.DataFrame.from_dict(weekHistory)
