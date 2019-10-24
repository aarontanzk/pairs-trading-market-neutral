import time
from alphavantageFunctions import getAverageAlphaVantageDataframe
import pandas as pd
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

def plotCointegratedPairs(equity1, equity2):
    time.sleep(30) #alphavantage time lock
    print("-------------------------- PLOTTING plotCointegratedPairs():--------------------------------")
    print("to plot and verify if a pair are truly cointegrated - the absolute ratio has little significance, hence z-score plotZScore() should be used for signal generation")
    
    #get data
    eq1 = getAverageAlphaVantageDataframe(equity1)
    eq2 = getAverageAlphaVantageDataframe(equity2)
    combinedData = pd.concat([eq1, eq2], axis=1)
    combinedData = combinedData.dropna()

    #get coint pvalue
    score, pvalue, _ = coint(combinedData[equity1] ,combinedData[equity2] )
    print("Cointegrated p-value: " + str(pvalue))
    combinedData['ratios'] = combinedData[equity1]  / combinedData[equity2]
    combinedData = combinedData.iloc[::-1] # correct timeline

    #plot
    combinedData['ratios'].plot()
    plt.axhline(combinedData['ratios'].mean())
    plt.legend([' Ratio'])
    plt.show()

def plotZScore(equity1, equity2):
    #get data
    eq1 = getAverageAlphaVantageDataframe(equity1)
    eq2 = getAverageAlphaVantageDataframe(equity2)
    combinedData = pd.concat([eq1, eq2], axis=1)
    combinedData = combinedData.dropna()

    #get ratios and zscore
    combinedData['ratios'] = combinedData[equity1] / combinedData[equity2]
    combinedData = combinedData.iloc[::-1] # correct timeline

    print(combinedData)
    print(zscore(combinedData['ratios']))

    #plot
    zscore(combinedData['ratios']).plot()
    plt.axhline(zscore(combinedData['ratios']).mean())
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='green')
    plt.show()
