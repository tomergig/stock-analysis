import pandas as pd


def sp500_data():
    sp500 = pd.read_csv('SP500_19500103_20240419.txt',
                        names=['symbol', 'date', 'open', 'high', 'low', 'close', 'volume'],
                        usecols=['date', 'open', 'high', 'low', 'close', 'volume'],
                        index_col='date',
                        parse_dates=True)

    sp500['interest'] = sp500['close'] / sp500['open'] - 1
    sp500 = sp500[sp500['interest'] != 0]
    return sp500