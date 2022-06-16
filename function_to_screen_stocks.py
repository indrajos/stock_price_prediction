import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf


def market_screener(list_of_tickers):
    """
    start_date = (year, month, day)
    list_of_tickers = dataframe of the stock tickers with a column name ['Symbol']

    function scrapes historical information from Yagoo Finanse by a given ticker,
    analyzes by 50, 100, 150 and 200 days moving averages and returns only those tickers
    which meets specified conditions
    """
    # Defining periods
    yf.pdr_override()
    start = dt.datetime(2020, 1, 1)
    now = dt.datetime.now()

    # Structure pf required table
    exportList = pd.DataFrame(columns=[
        'Stock'
        , "50 Day MA"
        , "150 Day Ma"
        , "200 Day MA"
        , "52 Week Low"
        , "52 week High"
    ])

    # df = pd.DataFrame({"Symbol": list_of_tickers})
    df = pd.DataFrame()
    for i in list_of_tickers:
        stock = [i]

        try:
            df = pdr.get_data_yahoo(stock, start, now)

            SMAused = [50, 150, 200]
            for x in SMAused:
                sma = x
                df["SMA_" + str(sma)] = round(df.iloc[:, 4].rolling(window=sma).mean(), 2)

            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = min(df["Adj Close"][-260:])
            high_of_52week = max(df["Adj Close"][-260:])
            try:
                moving_average_200_20 = df["SMA_200"][-20]

            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            if currentClose > moving_average_150 > moving_average_200:
                cond_1 = True
            else:
                cond_1 = False
            # Condition 2: 150 SMA and > 200 SMA
            if moving_average_150 > moving_average_200:
                cond_2 = True
            else:
                cond_2 = False
            # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
            if moving_average_200 > moving_average_200_20:
                cond_3 = True
            else:
                cond_3 = False
            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            if moving_average_50 > moving_average_150 > moving_average_200:
                # print("Condition 4 met")
                cond_4 = True
            else:
                # print("Condition 4 not met")
                cond_4 = False
            # Condition 5: Current Price > 50 SMA
            if currentClose > moving_average_50:
                cond_5 = True
            else:
                cond_5 = False
            # Condition 6: Current Price is at least 30% above 52 week low
            # (Many of the best are up 100-300% before coming out of consolidation)
            if currentClose >= (1.3 * low_of_52week):
                cond_6 = True
            else:
                cond_6 = False
            # C ondition 7: Current Price is within 25% of 52 week high
            if currentClose >= (.75 * high_of_52week):
                cond_7 = True
            else:
                cond_7 = False
            # Condition 8: IBD RS rating >70 and the higher the better

            if cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7:
                exportList = exportList.append({'Stock': stock, "50 Day MA": moving_average_50,
                                                "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200,
                                                "52 Week Low": low_of_52week, "52 week High": high_of_52week},
                                               ignore_index=True)
        except Exception:
            print("No data on " + stock)

    print()
    print(exportList)


if __name__ == "__main__":

    list = [
	'AXP','AAPL','BA','CAT','CSCO','CVX','XOM','GS','HD','IBM','INTC','JNJ','KO',
	'SIDU', 'BYND', 'GOLD', 'HOOD', 'EVOK', 'SPOT', 'OKE', 'WWE', 'SRNE', 'ROKU', 'ACAD', 'SNAP', 'DYN', 'OLN',
	'CVNA', 'TWTR', 'MULN', 'AERC', 'CHWY', 'PINS', 'AMZN', 'AMC', 'AMAT', 'GOOG', 'NIO', 'LI', 'SQ', 'TSM', 'BAC',
	'T', 'ARCT', 'GME', 'TSLA', 'INTC', 'PBR', 'PLTR', 'RBLX', 'KGC', 'ABEV', 'NOK', 'AAL', 'BBD', 'SNAP', 'NVDA',
	'NLY', 'SOFI', 'ITUB', 'CCL', 'F', 'AMD', 'DIDI'
]

    market_screener(list)
