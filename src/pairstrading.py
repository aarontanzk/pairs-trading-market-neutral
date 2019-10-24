from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from datetime import datetime
import time
import pandas as pd
import numpy as np
from enum import Enum
from statsmodels.tsa.stattools import coint
from config import ALPHAVANTAGE_APIKEY, eqArr , INTERVAL_1,INTERVAL_15,INTERVAL_60,OUTPUT_SIZE_FULL,PRICE_CLOSE,OPEN ,HIGH,LOW,CLOSE,VOLUME, NUM_DAYS
from plotFunctions import plotCointegratedPairs, plotZScore
from alphavantageFunctions import getAverageAlphaVantageDataframe

ts = TimeSeries(key=ALPHAVANTAGE_APIKEY, output_format='pandas')
ti = TechIndicators(key=ALPHAVANTAGE_APIKEY, output_format='pandas')

def convertDateIndex(df):
    convertedDate = []
    for i in df:
        newDate = i + ":00"
        convertedDate.append(newDate)

    return convertedDate

def getCorrelationValue(column1, column2):
    return column1.corr(column2)

def getCointegrationScore(equity1, equity2):
    score, pvalue, _ = coint(equity1, equity2)

    return score

def getCointegrationPvalue(equity1, equity2):
    score, pvalue, _ = coint(equity1, equity2)

    return pvalue

def zscore(series):
    return (series - series.mean()) / np.std(series)

def getZScoreSignal(equity1, equity2):
    eq1 = getAverageAlphaVantageDataframe(equity1)
    eq2 = getAverageAlphaVantageDataframe(equity2)
    combinedData = pd.concat([eq1, eq2], axis=1)
    combinedData = combinedData.dropna()

    combinedData['ratios'] = combinedData[equity1] / combinedData[equity2]
    combinedData = combinedData.iloc[::-1] # correct timeline
    combinedData['z'] = zscore(combinedData['ratios'])

    signal = combinedData['z'].iloc[-1]
    print(signal)
    if (signal < 0): # buy bc expect to revert to mean ratio
        buysell = "Buy the ratio(" + str(signal) + ") ---> Buy " + equity1 + " Sell " + equity2
        return buysell
    else:
        buysell = "Sell the ratio(" + str(signal) + ") ---> Sell " + equity1 + " Buy " + equity2
        return buysell

def getCorrelationAndCointegratedPairs(equity1, equity2):
    print("-------------------------- getCorrelationAndCointegratedPairs() --------------------------------")
    time.sleep(30) #alphavantage time lock

    priceData, priceMetadata = ts.get_daily(symbol=equity1, outputsize=OUTPUT_SIZE_FULL)
    priceData['avg1'] = (priceData[HIGH] + priceData[LOW])/2 #assume midpoint of high and low is executed price
    priceData.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData = priceData.head(NUM_DAYS)
    
    priceData2, priceMetadata2 = ts.get_daily(symbol=equity2, outputsize=OUTPUT_SIZE_FULL)
    priceData2['avg2'] = (priceData2[HIGH] + priceData2[LOW])/2 #assume midpoint of high and low is executed price
    priceData2.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData2 = priceData2.head(NUM_DAYS)

    combinedData = pd.concat([priceData, priceData2], axis=1)
    combinedData = combinedData.dropna()

    corr = getCorrelationValue(combinedData['avg1'], combinedData['avg2'])
    pvalue =  getCointegrationPvalue(combinedData['avg1'], combinedData['avg2'])

    print(equity1 + " & " + equity2 + " correlation: " + str(corr) + " coint: " + str(pvalue))
    #print(combinedData)

    return [corr, pvalue, equity1, equity2]

def getAllPairs():
    print("-------------------------- getAllPairs() --------------------------------")
    MIN_PVALUE = 0.05
    correlationArr = []

    for i in range(len(eqArr)):
        for j in range(len(eqArr)):
            if (eqArr[i]['name'] != eqArr[j]['name'] ):
                corrListObj = getCorrelationAndCointegratedPairs(eqArr[i]['name'] , eqArr[j]['name'] )
                print(corrListObj)
                if (corrListObj[1] < MIN_PVALUE):
                    correlationArr.append(corrListObj)


    return correlationArr

def mainzz():

    #res = equities_correlation()
    #print(res)
    res = [[0.8303010316568781, 0.008999534116927945, 'GOOGL', 'NKE'], [0.8465877548675863, 0.014318468108434462, 'GOOGL', 'AMZN'], [0.9230483904816502, 0.013301862473843282, 'NKE', 'AMZN'], [0.8677516812739479, 0.03705038629479192, 'COKE', 'PEP'], [0.8676595604577452, 0.027009363509322395, 'PEP', 'COKE'], [0.9217183557694564, 0.027048611523533345, 'AMZN', 'NKE']]
    

    equity1 = "COKE"
    equity2 = "PEP"
    #plotCointegratedPairs(equity1,equity2)
    #res = getCorrelationAndCointegratedPairs(equity1,equity2)
    #print(res)
    '''
    
    for x in range(len(res)):
        signalResult = getZScoreSignal(res[x][2], res[x][3])
        print(signalResult)
    '''
    #signalResult = getZScoreSignal(equity1, equity2)
    getAllPairs()
 
#mainzz()
