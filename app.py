# -*- coding: utf-8 -*-
"""
Created on 

@author: 
"""
import os
import pandas as pd
import numpy as np

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


class YahooDataService():
    def __init__(self, tickers):
        self.all_tickers = tickers;
        self.selected_stocks = yf.Tickers(tickers)
        self.tickers = self.all_tickers.split(" ")
    
    def getOneYearHistoryForList(self):
        selected_history = {}
        for index in range(len(self.tickers)):
            selected_history[self.tickers[index]] = self.selected_stocks.tickers[index].history(period="1y")
        return selected_history

class RequestConvertor():
    def convertToString(self, d):
        string =" "
        return (string.join(d.values()))
    
class DataPointCalculator():
    def __init__(self, selected_history):
        self.selected_history = selected_history
    
    def getIntradayChangeInfo(self, data_set):
        data_set["Intraday Change"] = data_set["Open"] - data_set["Close"]
        data_set["Intraday Pct Change"] = data_set["Intraday Change"] / data_set["Open"]
        
        previous_day_change = 0
        previous_day_pct_change = 0
        all_previous_day_change = []
        all_previous_day_pct_change = []
        
        for index, row in data_set.iterrows():
            all_previous_day_change.append(previous_day_change)
            all_previous_day_pct_change.append(previous_day_pct_change)
            previous_day_change = row["Intraday Change"]
            previous_day_pct_change = row["Intraday Pct Change"]
            
        data_set["Previous Day Change"] = all_previous_day_change
        data_set["Previous Day Pct Change"] = all_previous_day_pct_change
        return data_set
    
    def updateFiveDays(self, current_day, five_days):
        if(five_days.size == 5):
            five_days["1"] = five_days["2"]
            five_days["2"] = five_days["3"]
            five_days["3"] = five_days["4"]
            five_days["4"] = five_days["5"]
            five_days["5"] = current_day
        else:
            five_days[str(five_days.size + 1)] = current_day
        return five_days
    
    def getFiveDayAverageForIntraChange(self, data_set):
        previous_five_days = pd.Series(dtype="float64")
        previous_five_days_averages = []
        for index, row in data_set.iterrows():
            previous_five_days_averages.append(previous_five_days.mean())
            previous_five_days = self.updateFiveDays(row["Intraday Pct Change"], previous_five_days)
            
        data_set["Previous Five Day Average Pct Change"] = previous_five_days_averages
        data_set["Previous Five Day Average Pct Change"].fillna(0, inplace=True)
        return data_set
    
    def getAllCalculatedDataPoints(self):
        for key, history in self.selected_history.items():
            self.getIntradayChangeInfo(history)
            self.getFiveDayAverageForIntraChange(history)
        return self.selected_history
    
    
class DataModeler():
    
    def __init__(self, features, target):
        self.features = features;
        self.target = target;
    
    def createLinearRegression(self, X, y):
        lr = LinearRegression()
        lr.fit(X, y)
        return lr

    def testLinearRegression(self, model, X_train, X_test, y_train, y_test):
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        preds = model.predict(X_test)
        score = explained_variance_score(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        rmse = math.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        
        print("Train Score: {}\nTest Score: {}"
              .format(train_score, test_score))
        print("Score Details = {:.5f} | MAE = {:.3f} | RMSE = {:.3f} | R2 = {:.5f}"
              .format(score, mae, rmse, r2))
        print("\n")
        
    
    def conductLinearRegressionAnalysis(self, data_set):
        X = data_set[self.features]
        y = data_set[self.target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
        
        model= self.createLinearRegression(X_train, y_train)
        #self.testLinearRegression(model, X_train, X_test, y_train, y_test)
        
        return model
    
    def getAllModels(self, data_set):
        models = {}
        for key, history in data_set.items():
            #print("For: {}".format(key))
            models[key] = self.conductLinearRegressionAnalysis(history)
        
        return models
    
class Predictor():
    def __init__(self, features, data_set, models):
        self.features = features;
        self.data_set = data_set;
        self.models = models;
    
    def createPredictions(self, model, data_set):
        return model.predict(data_set[self.features])
    
    def getFinalPredictions(self):
        self.final_predictions = pd.Series(dtype="float64")
        for key, values in self.data_set.items():
            values["Prediction"] = self.createPredictions(self.models[key], values)
            self.final_predictions[key] = values.iloc[-1]["Prediction"]
        return self.final_predictions
    
    def getRecommendation(self):
        self.getFinalPredictions();
        return (self.final_predictions.idxmax(), self.final_predictions.max())
    
    
class stockpred(Resource):
    def get(self):
        requestConvertor = RequestConvertor();
        tickers = requestConvertor.convertToString(request.args);
        
        dataService = YahooDataService(tickers);
        selected_history = dataService.getOneYearHistoryForList();
        
        dataPointCalculator = DataPointCalculator(selected_history);
        selected_history = dataPointCalculator.getAllCalculatedDataPoints();
        
        features = ["Previous Day Pct Change", "Previous Day Change","High", "Low", "Volume", "Open", "Previous Five Day Average Pct Change"]
        target = "Intraday Pct Change"
        dataModeler = DataModeler(features, target)
        models = dataModeler.getAllModels(selected_history)
        
        predictor = Predictor(features, selected_history, models)
        recommendation = predictor.getRecommendation()
        
        return recommendation[0]



# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(stockpred, '/stockpred')



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)