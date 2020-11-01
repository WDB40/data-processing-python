# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 19:12:23 2020

@author: mattq
"""
import pandas as pd
import Ondemand
from Config import api_key, end_point

od = Ondemand.OnDemandClient(api_key, end_point)

def currentData(s):
    
    quotes = od.quote(s)['results']
    df = pd.DataFrame.from_dict(quotes)

    return (df)