# work in progress

import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from plotly.colors import n_colors
import statsmodels.api as sm
from data_preprocess import sp500_data

NLAGS = 365
LOWER = 0.15
UPPER = 0.85
REPETITIONS = 1000
INITIAL_INVESTMENT = 1
data = sp500_data()

# one can see low correlations between past days
acf_all = sm.tsa.acf(data['interest'], nlags=NLAGS, adjusted=True)[1:]
px.scatter(acf_all, title='sp500 auto-correlation from ~1950').update_layout(
    xaxis_title="lags", yaxis_title="correlation").show()
# add mean and var

# comparing the final value distributions for each starting point from the real sp500 data
colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 9, colortype='rgb')
fig = go.Figure()
for numYears, color in zip(range(1, 10), colors):
    interest_5 = []
    for i in range(len(data)):
        splice = data[i:i + 365 * numYears]
        profit = np.cumprod(np.insert(splice['interest'] + 1, 0, INITIAL_INVESTMENT))[-1]
        interest_5.append(profit)
    fig.add_trace(go.Violin(x=100 * (np.array(interest_5) - 1) / numYears, line_color=color, name=numYears))
fig.update_traces(orientation='h', side='positive', width=3, points=False)
fig.update_layout(title="interest per year for different investment periods ", yaxis_title="years of investing",
                  xaxis_title="yearly interest %")
fig.show()

fig = go.Figure()
for numYears, color in zip(range(1, 10), colors):
    interest_5 = []
    for i in range(len(data)):
        splice = np.random.choice(data['interest'], replace=True, size=365 * numYears)
        profit = np.cumprod(np.insert(splice + 1, 0, INITIAL_INVESTMENT))[-1]
        interest_5.append(profit)
    fig.add_trace(go.Violin(x=100 * (np.array(interest_5) - 1) / numYears, line_color=color, name=numYears))
fig.update_traces(orientation='h', side='positive', width=3, points=False)
fig.update_layout(title="interest per year for different investment periods for a randomized sample  ",
                  yaxis_title="years of investing", xaxis_title="yearly interest %")
fig.show()


def increase_correlation(array, lag, correlation):
    """ this function works wel only on small fractions (0.3 0.4) still need to check how to decrease correlation"""
    insertion_array = [array[i % lag] for i in range(round((len(array) - lag) * abs(correlation)))]
    array[lag:len(insertion_array) + lag] = insertion_array
    return array
