from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from datetime import datetime
import time
import pandas as pd

ALPHAVANTAGE_APIKEY = "392PM7H6LAUQ50C3"
ts = TimeSeries(key=ALPHAVANTAGE_APIKEY, output_format='pandas')
ti = TechIndicators(key=ALPHAVANTAGE_APIKEY, output_format='pandas')

# CONFIG
SYMBOL = "MSFT"
INTERVAL_1 = "1min"
INTERVAL_15 = "15min"
OUTPUT_SIZE = "full"
PRICE_CLOSE = "4. close"

def convertDateIndex(df):
    convertedDate = []
    for i in df:
        newDate = i + ":00"
        convertedDate.append(newDate)

    return convertedDate

def macd():
    #data handling
    macdData, macdMetadata = ti.get_macd(symbol=SYMBOL,interval=INTERVAL_15)
    priceData, priceMetadata = ts.get_intraday(symbol=SYMBOL,interval=INTERVAL_15, outputsize=OUTPUT_SIZE)
    macdData.index = convertDateIndex(macdData.index)
    combinedData = pd.concat([macdData, priceData], axis=1)
    combinedData = combinedData.dropna()

    #signal generation
    signalArr = []
    for i in combinedData['MACD']:
        if i <= 0.30:                 #strong buy
            signalArr.append(2)
        elif i<= 0.45 and i>0.30:       #buy
            signalArr.append(1)
        elif i>= 0.55 and i<0.70:       #sell
            signalArr.append(-1)
        elif (i >= 0.70):             #strong sell
            signalArr.append(-2)
        else:
            signalArr.append(0)
    combinedData['macdSignal'] = signalArr

    #plot
    fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
    plot1a, = ax1.plot(combinedData['MACD_Hist'], color="orange", label = 'MACD Historical')
    plot1b, = ax1.plot(combinedData['MACD_Signal'], color="blue", label='MACD Signal Line')
    plot1c, = ax1.plot(combinedData['MACD'], color="green", label='MACD ')
    ax1.legend(handles=[plot1a, plot1b, plot1c])
    ax1.set_title('MACD, Historical & Signal')

    plot2a, = ax2.plot(combinedData['macdSignal'], color = "green", label = "MACD")
    ax3 = ax2.twinx() 
    ax3.set_ylabel('Stock Price', color='grey')
    ax3.tick_params(axis='y', labelcolor='grey')
    plot2b, = ax3.plot(combinedData[PRICE_CLOSE], color= "grey", label = "CLOSE PRICE" )
    ax2.legend(handles=[plot2a, plot2b])
    ax2.set_title('MACD Signal & Stock Price')

    plt.show()

def stoch():
    #data handling
    stochData, stochMetadata = ti.get_stoch(symbol=SYMBOL,interval=INTERVAL_15)
    priceData, priceMetadata = ts.get_intraday(symbol=SYMBOL,interval=INTERVAL_15, outputsize=OUTPUT_SIZE)
    stochData.index = convertDateIndex(stochData.index)
    combinedData = pd.concat([stochData, priceData], axis=1)
    combinedData = combinedData.dropna()

    #signal generation
    signalArr = []
    for i in combinedData['SlowK']:
        if i <= 20:
            signalArr.append(1)
        elif (i >= 80):
            signalArr.append(-1)
        else:
            signalArr.append(0)
    combinedData['stochSignal'] = signalArr

    #plot
    fig, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)
    ax1.plot(combinedData['SlowK'])
    ax1.set_title("Stochastic Oscillator Raw")
    ax2.plot(combinedData['stochSignal'])
    ax2.set_title('Stoch Signal')
    ax3.plot(combinedData[PRICE_CLOSE])
    ax3.set_title('Stock Price')

    plt.show()

def rsi():
    #data handling
    rsiData, rsiMetadata = ti.get_rsi(symbol=SYMBOL,interval=INTERVAL_15)
    priceData, priceMetadata = ts.get_intraday(symbol=SYMBOL,interval=INTERVAL_15, outputsize=OUTPUT_SIZE)
    rsiData.index = convertDateIndex(rsiData.index)
    combinedData = pd.concat([rsiData, priceData], axis=1)
    combinedData = combinedData.dropna()

    #signal generation
    signalArr = []
    for i in combinedData['RSI']:
        if i <= 30:                 #strong buy
            signalArr.append(2)
        elif i<= 45 and i>30:       #buy
            signalArr.append(1)
        elif i>= 55 and i<70:       #sell
            signalArr.append(-1)
        elif (i >= 70):             #strong sell
            signalArr.append(-2)
        else:
            signalArr.append(0)
    combinedData['rsiSignal'] = signalArr

    #plot
    fig, (ax1, ax3) = plt.subplots(nrows = 2, ncols = 1)
    ax1.plot(combinedData['rsiSignal'], label='RSI Signal')
    ax1.set_title('RSI BUY/SELL Signal & Stock Price')
    ax2 = ax1.twinx() 
    ax2.set_ylabel('Stock Price', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.plot(combinedData[PRICE_CLOSE], color='red', label='CLOSE PRICE')
    
    ax3.plot(combinedData['RSI'])
    ax3.set_title('RSI')
    
    plt.legend(loc='best')
    plt.show()

def main():
    macd()
    #rsi()
    #stoch()
 
main()
