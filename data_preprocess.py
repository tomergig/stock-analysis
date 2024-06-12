import pandas as pd
import yfinance as yf




def sp500_data():
    """

    :return: Data frame with columns : Date, Open, High, Low, Close, Volume, interest
    which specifies sp500 values using EOD downloaded data from 1962/1 to 2024/4
    """
    sp500 = pd.read_csv('SP500_19500103_20240419.txt',
                        names=['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'],
                        usecols=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'],
                        index_col='Date',
                        parse_dates=True)

    sp500['interest'] = sp500['Close'] / sp500['Open'] - 1
    sp500 = sp500[sp500['interest'] != 0]
    return sp500


def sp500_data_yfinance():
    """

    :return: Data frame with columns : Date, Open, High, Low, Close, Volume, interest
    which specifies sp500 values using yfinance
    """
    sp500 = yf.download("^GSPC", start="1950-01-01", end="2024-05-01")
    sp500['interest'] = sp500['Close'] / sp500['Open'] - 1
    sp500 = sp500[sp500['interest'] != 0]
    return sp500

def sp5003x_data():
    """

    :return: Data frame with columns : Date, Open, High, Low, Close, Volume, interest
    which specifies "Direxion Daily S&P 500 Bull 3X Shares" values using yfinance
    """
    sp5003x = yf.download("SPXL", start="1950-01-01", end="2024-05-01")
    sp5003x['interest'] = sp5003x['Close'] / sp5003x['Open'] - 1
    sp5003x = sp5003x[sp5003x['interest'] != 0]
    return sp5003x




if __name__ == '__main__':
    a=sp500_data()
    b=sp500_data_yfinance()
    c=sp5003x_data()