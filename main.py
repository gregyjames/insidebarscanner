import pandas as pd
import yfinance as yf
import numpy as np
from multiprocessing import Pool

def getData(x):
    prices = yf.download(tickers=x, period="5d", interval="1d", auto_adjust=False, prepost=False, threads=True, progress=False, show_error=False)[-2:]

    open = prices["Open"]
    close = prices["Close"]
    if len(open) > 1:
        if (close[0]-open[0]) > (close[1]-open[1]):
            return x


if __name__ == '__main__':
    data = pd.read_csv("data.csv", header=0).dropna()
    #Add filters
    #dfiltered = (data[data["Market Cap"] > 10000000000])["Symbol"].to_list()
    tickers = []
    #Modify number to fit your system
    with Pool(32) as p:
        tickers = p.map(getData, data)
    tickers1 = list(filter(lambda x: x != None, tickers))
    print(tickers1)