
from data_preprocess import sp500_data,sp5003x_data


# Get empirical sp500 data from EOD downloaded file
data_reg = sp500_data()
# Gets a 3x version of the sp500 from "Direxion Daily S&P 500 Bull 3X Shares"
data3x= sp5003x_data()

data = data3x.join(data_reg,how='inner',lsuffix='_3')
YEARS = 5
INVESTMENT_PERIOD = 365 * YEARS
INTEREST_VALUES = data_reg['interest']
INTEREST_VALUES1X = data['interest']
INTEREST_VALUES3x = data['interest_3']
COMMISSION = 0.97
REPETITIONS = 1000

