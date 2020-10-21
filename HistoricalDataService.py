# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 19:14:28 2020

@author: mattq
"""
import pandas as pd
import Ondemand
from Config import api_key, end_point
from datetime import date, timedelta


od = Ondemand.OnDemandClient(api_key, end_point)

def historicData(s, dP):
    today = date.today()
    pDate = today - timedelta(days=dP)
    previousDay = today - timedelta(days=1)
    sDate = date(year = pDate.year, month=pDate.month, day=pDate.day)
    eDate = date(year = previousDay.year, month=previousDay.month, day=previousDay.day)
    sDate = sDate.strftime("%Y%m%d")
    #params=dict(startDate=sDate, endDate=eDate)
    
    #weekHistory = od.history(s, 'daily')['results']
    weekHistory = od.history(s, 'daily', startDate=sDate, endDate=eDate)['results']
    df = pd.DataFrame.from_dict(weekHistory)

    return (df)