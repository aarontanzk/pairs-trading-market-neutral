## Pairs Trading / Long Short Equity in Python

Market Neutral Strategy to identify correlated / cointegrated pairs.

Long position on undervalued, short position on overvalued.

Results:
23 OCT 19
Buy the signal(-1.3932782671776829) ---> Buy GOOGL Sell NKE
Buy the signal(-0.31384218669585223) ---> Buy GOOGL Sell AMZN
Sell the signal(1.2043485000702945) ---> Sell NKE Buy AMZN
Sell the signal(0.6119628429995375) ---> Sell COKE Buy PEP
Buy the signal(-0.6977745731131804) ---> Buy PEP Sell COKE
Buy the signal(-1.2208466945241816) ---> Buy AMZN Sell NKE




Production & Scability:
1) Build Docker Image
2) Deploy on cloud server
3) Scale using Kubernates (OpenShift / AWS EKS / GCloud)



To run gunicorn:
gunicorn app:app --config=config.py

To run script:
Install setup.py
python .\src\pairstrading.py
127.0.0.1:8080/

To run tests:
python .\src\tests.py

Todo:
Backtest / Feature Engineering