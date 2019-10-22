from technicalanalysis import getZScoreSignal

def correlationTest():
    corr = pd.DataFrame([[1, 1], [2, 2], [3,3],[4,4], [5,5], [6,6]], columns=['col1', 'col2'])
    inverseCorr = pd.DataFrame([[1, 2], [2, 1]], columns=['col1', 'col2'])

    print("Correlation Test - To ensure function works correctly")
    print(getCorrelationValue(corr ['col1'], corr ['col2']))
    print(getCorrelationValue(inverseCorr ['col1'], inverseCorr ['col2']))
    #print(corr)

def getZScoreSignalTest():
    equity1 = "COKE"
    equity2 = "PEP"
    getZScoreSignal(equity1, equity2)
    
def main():
    correlationTest()

main()