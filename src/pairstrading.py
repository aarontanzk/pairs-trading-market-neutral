from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from datetime import datetime
import time
import pandas as pd
import numpy as np
from enum import Enum
from statsmodels.tsa.stattools import coint

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

ALPHAVANTAGE_APIKEY = "392PM7H6LAUQ50C3"
ts = TimeSeries(key=ALPHAVANTAGE_APIKEY, output_format='pandas')
ti = TechIndicators(key=ALPHAVANTAGE_APIKEY, output_format='pandas')

# CONFIG
SYMBOL = "MSFT"
SYMBOL2 = "AAPL"
NUM_DAYS = 600


eqArr = [
    {
        "name": "MSFT",
        "sector": "Technology"
    },
    {
        "name": "AAPL",
        "sector": "Technology"
    },
    {
        "name": "GOOGL",
        "sector": "Technology"
    },
    {
        "name": "NKE",
        "sector": "Apparel"
    },
    {
        "name": "TRV",
        "sector": "Travel"
    },
    {
        "name": "COKE",
        "sector": "Travel"
    },
    {
        "name": "PEP",
        "sector": "Travel"
    },
       {
        "name": "AMZN",
        "sector": "Technology"
    },
    {
        "name": "NVDA",
        "sector": "Chip"
    },
    {
        "name": "AMD",
        "sector": "Travel"
    },

]

#ENUM
INTERVAL_1 = "1min"
INTERVAL_15 = "15min"
INTERVAL_60 = "60min"
OUTPUT_SIZE_FULL = "full"
PRICE_CLOSE = "4. close"

OPEN = "1. open"
HIGH = "2. high"
LOW = "3. low"
CLOSE = "4. close"
VOLUME = "5. volume"

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

def plotCointegratedPairs(equity1, equity2):
    time.sleep(30) #alphavantage time lock

    priceData, priceMetadata = ts.get_daily(symbol=equity1, outputsize=OUTPUT_SIZE_FULL)
    priceData['avg1'] = (priceData[HIGH] + priceData[LOW])/2 #assume midpoint of high and low is executed price
    priceData.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData = priceData.head(NUM_DAYS)
    
    priceData2, priceMetadata2 = ts.get_daily(symbol=equity2, outputsize=OUTPUT_SIZE_FULL)
    priceData2['avg2'] = (priceData2[HIGH] + priceData2[LOW])/2 #assume midpoint of high and low is executed price
    priceData2.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData2 = priceData2.head(NUM_DAYS)

    S1 = priceData
    S2 = priceData2

    score, pvalue, _ = coint(S1, S2)
    print(pvalue)
    ratios = S1 / S2
    ratios.plot()
    plt.axhline(ratios.mean())
    plt.legend([' Ratio'])
    plt.show()

def zscore(series):
    return (series - series.mean()) / np.std(series)

def plotZScore(equity1, equity2):
    eq1 = getAverageAlphaVantageDataframe(equity1)
    eq2 = getAverageAlphaVantageDataframe(equity2)
    combinedData = pd.concat([eq1, eq2], axis=1)
    combinedData = combinedData.dropna()

    combinedData['ratios'] = combinedData[equity1] / combinedData[equity2]
    combinedData = combinedData.iloc[::-1] # correct timeline

    print(combinedData)
    print(zscore(combinedData['ratios']))
    zscore(combinedData['ratios']).plot()
    plt.axhline(zscore(combinedData['ratios']).mean())
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='green')
    plt.show()

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
    
def getAverageAlphaVantageDataframe(equity):
    time.sleep(30) #alphavantage time lock
    equityStr = equity

    priceData, priceMetadata = ts.get_daily(symbol=equity, outputsize=OUTPUT_SIZE_FULL)
    priceData[equity] = (priceData[HIGH] + priceData[LOW])/2 #assume midpoint of high and low is executed price
    priceData.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData = priceData.head(NUM_DAYS)
    #print(priceData)
    return priceData

def getCorrelation(equity1, equity2):
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

    #corr = combinedData['avg1'].corr(combinedData['avg2'])
    corr = getCorrelationValue(combinedData['avg1'], combinedData['avg2'])
    print("Correlation between " + equity1 + " & " + equity2)
    print(corr)
    pvalue =  getCointegrationPvalue(combinedData['avg1'], combinedData['avg2'])
    #print(combinedData)

    return [corr, pvalue, equity1, equity2]

def equities_correlation():
    print("-------------------------- RUNNING equities_correlation() --------------------------------")
    MIN_PVALUE = 0.05
    correlationArr = []

    for i in range(len(eqArr)):
        for j in range(len(eqArr)):
            if (eqArr[i]['name'] != eqArr[j]['name'] ):
                corrListObj = getCorrelation(eqArr[i]['name'] , eqArr[j]['name'] )
                print(corrListObj)
                if (corrListObj[1] < MIN_PVALUE):
                    correlationArr.append(corrListObj)


    return correlationArr

def splitData(equity1, equity2):
    print("-------------------------- RUNNING SPLITDATA() --------------------------------")
    eq1 = getAverageAlphaVantageDataframe(equity1)
    eq2 = getAverageAlphaVantageDataframe(equity2)

    ratios = eq1 / eq2
    print(len(ratios))
    train = ratios[:1762]
    test = ratios[1762:]

    ratios_mavg5 = train.rolling(window=5,center=False).mean()
    ratios_mavg60 = train.rolling(window=60,center=False).mean()
    std_60 = train.rolling(window=60,center=False).std()
    zscore_60_5 = (ratios_mavg5 - ratios_mavg60)/std_60
    plt.figure(figsize=(15,7))
    plt.plot(train.index, train.values)
    plt.plot(ratios_mavg5.index, ratios_mavg5.values)
    plt.plot(ratios_mavg60.index, ratios_mavg60.values)
    plt.legend(['Ratio','5d Ratio MA', '60d Ratio MA'])
    plt.ylabel('Ratio')
    plt.show()

def main():

    #res = equities_correlation()
    res = [[0.8303010316568781, 0.008999534116927945, 'GOOGL', 'NKE'], [0.8465877548675863, 0.014318468108434462, 'GOOGL', 'AMZN'], [0.9230483904816502, 0.013301862473843282, 'NKE', 'AMZN'], [0.8677516812739479, 0.03705038629479192, 'COKE', 'PEP'], [0.8676595604577452, 0.027009363509322395, 'PEP', 'COKE'], [0.9217183557694564, 0.027048611523533345, 'AMZN', 'NKE']]
    #print(res)
    #plotZScore("COKE", "PEP")
    equity1 = "COKE"
    equity2 = "PEP"
    for x in range(len(res)):
        signalResult = getZScoreSignal(res[x][2], res[x][3])
        print(signalResult)
    #signalResult = getZScoreSignal(equity1, equity2)
  
 
main()
