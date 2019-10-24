import pandas as pd
from pairstrading import getZScoreSignal, getCorrelationAndCointegratedPairs, getCorrelationValue

def getCorrelationAndCointegratedPairsTest():
    print("-------------------------- RUNNING TEST - getCorrelationAndCointegratedPairsTest() --------------------------------")

    corr = pd.DataFrame([[1, 1], [2, 2], [3,3],[4,4], [5,5], [6,6]], columns=['col1', 'col2'])
    inverseCorr = pd.DataFrame([[1, 2], [2, 1]], columns=['col1', 'col2'])

    print("Correlation Test - To ensure function works correctly")
    print(getCorrelationValue(corr ['col1'], corr ['col2']))
    print(getCorrelationValue(inverseCorr ['col1'], inverseCorr ['col2']))
    #print(corr)

def getZScoreSignalTest():
    print("-------------------------- RUNNING TEST getZScoreSignalTest()--------------------------------")
    equity1 = "COKE"
    equity2 = "PEP"
    getZScoreSignal(equity1, equity2)
    
def main():
    getCorrelationAndCointegratedPairsTest()
    getZScoreSignalTest()

main()