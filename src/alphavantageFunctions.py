from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
from config import ALPHAVANTAGE_APIKEY, eqArr , INTERVAL_1,INTERVAL_15,INTERVAL_60,OUTPUT_SIZE_FULL,PRICE_CLOSE,OPEN ,HIGH,LOW,CLOSE,VOLUME, NUM_DAYS

ts = TimeSeries(key=ALPHAVANTAGE_APIKEY, output_format='pandas')
ti = TechIndicators(key=ALPHAVANTAGE_APIKEY, output_format='pandas')

def getAverageAlphaVantageDataframe(equity):
    time.sleep(30) #alphavantage time lock
    equityStr = equity

    priceData, priceMetadata = ts.get_daily(symbol=equity, outputsize=OUTPUT_SIZE_FULL)
    priceData[equity] = (priceData[HIGH] + priceData[LOW])/2 #assume midpoint of high and low is executed price
    priceData.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData = priceData.head(NUM_DAYS)

    return priceData

def getAllAlphaVantageDataFrame(equity):
    priceData, priceMetadata = ts.get_daily(symbol=equity1, outputsize=OUTPUT_SIZE_FULL)
    priceData['avg1'] = (priceData[HIGH] + priceData[LOW])/2 #assume midpoint of high and low is executed price
    #priceData.drop([OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)
    priceData = priceData.head(NUM_DAYS)

    return priceData