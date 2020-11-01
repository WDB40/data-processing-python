# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 19:57:17 2020

@author: mattq
"""


#import numpy as np
from sklearn.linear_model import LinearRegression

from sklearn.cluster import KMeans                        # k-means clustering 
from sklearn.model_selection import train_test_split      # train/test data
from sklearn.neighbors import KNeighborsClassifier        # k-NN classification 
from sklearn.linear_model import LogisticRegression  

def regPredict(X,y,z):

   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
   
   lr=LinearRegression()
   lr.fit(X_train, y_train)
   pred = lr.predict(z)
   print(lr.score(X_train,y_train))
   print(lr.score(X_test,y_test))
 
    
    # knn = KNeighborsClassifier(n_neighbors=3) 
    # knn.fit(X_train, y_train)         
    # knn.score(X_train, y_train)
    # knn.score(X_test, y_test)            
    # pred = knn.predict(z)
    
    #model = LinearRegression().fit(x, y)
    #model.score(x, y)
    #r_sq = model.score(x, y)
    #y_pred = model.predict(x)
   return(pred)