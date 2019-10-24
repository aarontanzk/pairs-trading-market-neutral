from flask import Flask, request
from pairstrading import getAllPairs, getCorrelationAndCointegratedPairs, getZScoreSignal
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/api/allpairs')
def allPairsTrading():
   return getAllPairs()

@app.route('/api/checkpairs', methods=['GET'])
def checkPairs(): #127.0.0.1:5000/api/checkpairs?summary=COKE&change=PEP
    eq1 = request.args.get('eq1')
    eq2 = request.args.get('eq2')
    print (request.args.get('eq1'))
    print (request.args.get('eq2'))

    res =  getCorrelationAndCointegratedPairs(eq1, eq2)
    resStr =  eq1 + " & " + eq2 + " correlation: " + str(res[0]) + " coint: " + str(res[1])
    return resStr

@app.route('/api/pairsignal', methods=['GET'])
def pairSignal(): #127.0.0.1:5000/api/checkpairs?summary=COKE&change=PEP
    eq1 = request.args.get('eq1')
    eq2 = request.args.get('eq2')
    print (request.args.get('eq1'))
    print (request.args.get('eq2'))

    res =  getZScoreSignal(eq1, eq2)
    return res


if __name__ == '__main__':
   app.run()