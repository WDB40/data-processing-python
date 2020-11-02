# data-processing-python
Repository for the Data Processing in Python class project at the University of Iowa.

## Unqiue Installs Required
pip install yfinance

## Files in Project
The project contains 4 main files and they are listed below. All other files and folders can be ignored.

### Gathering Data.ipynb
This notebook goes through the data collection process used for this project. It also goes into the calculated fields that are used. There are visuals around the a few of the calculated fields.

### Creating_Model.ipynb
This notebook goes through the model creation process for this project. There are also visuals for seeing how the prediction matches up with the actual values.

### app.py
This is the application file that is used to run the applicaiton and make it accessible via an api. Since our models are created real time when the user hits our endpoints, we have much of what is covered in the previous two notebooks in this file as well.

### DPP Project.postman_collection.json
This file contains the 3 example calls to the app once it is running. It contains examples with 3, 5, and 10 different stocks as input. You can add and change tickers as you would like. The variable names in postman do not matter, but the tickers should be valid tickers.
