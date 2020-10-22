# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 22:29:19 2020

@author: mattq
"""




from CurrentDataService import currentData
from HistoricalDataService import historicData
from modelPredictService import regPredict
import pandas as pd





Symbol = input("Enter Stock Symbol: ")
Symbol.upper()
daysPast = input("Enter desired previous Days for analysis: ")
while True:
    try:
        daysPast = float(daysPast)
        break
    except ValueError:
        daysPast = input("Please enter desired Days again: ")



todayDF = currentData(Symbol)
historyDF = historicData(Symbol, daysPast)
today = pd.DataFrame(todayDF, columns=['open', 'high', 'low', 'volume'])

price = pd.DataFrame(historyDF, columns = ['close'])
var = pd.DataFrame(historyDF, columns = ['open', 'high', 'low', 'volume'])

print(regPredict(var, price, today))