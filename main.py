import pandas as pd
import yfinance as yf
import os
from multiprocessing import Pool
import contextlib

def check_insidebar(ticker,prices):
    open = prices["Open",ticker]
    close = prices["Close",ticker]
    if len(open) > 1:
        if (close[0]-open[0]) > (close[1]-open[1]):
            return True
        else: 
            return False
    else:
        return False

def getData(listTickers):
    #Suppress all output from yfinance
    with contextlib.redirect_stdout(None):
        #Get the prices for the list of symbols
        prices = yf.download(tickers=listTickers, period="5d", interval="1d", auto_adjust=False, prepost=False, threads=True, progress=False, show_error=False)[-2:]
        #List to hold processed symbols 
        processed = list(filter(lambda x: check_insidebar(x,prices), listTickers));
        
    return processed


if __name__ == '__main__':
    #Get the list of Symbols from the csv file
    data = (pd.read_csv("data.csv", header=0).dropna())["Symbol"].to_list()
    
    #Make the list of tickers into chunks of 20
    data_chunks = [data[x:x+20] for x in range(0, len(data), 20)]
    
    #Add filters
    #dfiltered = (data[data["Market Cap"] > 10000000000])["Symbol"].to_list()
    
    #List to hold processed symbols
    processed_tickers = []

    #Multiprocessing pool to use all the cores on cpu
    with Pool(processes=os.cpu_count() - 1) as p:
        #Map the function on the list of ticker chunks
        temp = p.map_async(getData, (data_chunks))
        #Get the results
        tickers = temp.get()

    #Flatten the list of lists
    flat_list = [item for sublist in tickers for item in sublist]

    #Print the list of tickers and the number
    print(flat_list)
    print(len(flat_list))