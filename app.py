# -*- coding: utf-8 -*-
"""
Created on 

@author: 
"""
import os
import pandas as pd

import json

from flask import Flask
from flask_restful import Api, Resource, request
import joblib

import yfinance as yf
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score, mean_absolute_error, r2_score, mean_squared_error

import pandas as pd
import numpy as np
import plotly.offline as plyo
import cufflinks as cf


port = int(os.getenv('PORT', '5000'))

app = Flask(__name__)
api = Api(app)

# argument parsing
#parser = reqparse.RequestParser()
#parser.add_argument('query')

# all_tickers = {"Input1": "WFC", "Input2": "MSFT", "Input3": "TSLA"}
# tickers=list(all_tickers.values())

     

# selected_stocks = yf.Tickers(all_tickers)


# all_tickers = "WFC MSFT INTC AMZN PYPL"
# selected_stocks = yf.Tickers(all_tickers)
# tickers = all_tickers.split(" ")




class stockpred(Resource):
    def get(self):
        tickers=request.args

        def convertToString(d):
            string =" "
            return (string.join(d.values()))      
        
        tickers=convertToString(tickers)
        
        
        return tickers






# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(stockpred, '/stockpred')



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)