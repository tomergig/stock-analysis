# %%
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.colors import n_colors

from analysis_functions import stats_per_period, probabiliy_losing, get_last
from data_preprocess import sp500_data

data = sp500_data()

INVESTMENT_PERIOD = 365 * 5
INTEREST_VALUES = data['interest'].values

leverages = np.linspace(1, 6, 30)
data = pd.DataFrame(index=leverages)
for leverage in leverages:
    binary_lost, last_value = stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, leverage, probabiliy_losing(0.5),
                                               get_last)
    data.at[leverage, 'probability to lose 50%'] = np.mean(binary_lost)
    data.at[leverage, 'probability for profit'] = np.mean(np.array(last_value) > 1)


# Displays the probability to lose 50% and the probability for profit as a function of leverage
px.line(data, y=['probability to lose 50%', 'probability for profit']).show()

# Displays the distribution of the total interest
# (with a log10 transform) as a function of leverage, the total interest
# the x-axis reflects the true value

colors = n_colors('rgb(5, 0, 200)', 'rgb(200, 10, 10)', 10, colortype='rgb')
fig = go.Figure()
leverages = np.linspace(1, 6, 11)
for leverage, color in zip(leverages, colors):
    last_value = stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, leverage, get_last)[0]
    fig.add_trace(go.Violin(x=np.log10(last_value), line_color=color, name=round(leverage, 3), spanmode='hard',
                            meanline_visible=True))
fig.update_traces(orientation='h', side='positive', width=3, points=False)
fig.add_annotation(x=-2, y=1, text="*The hover-info is for the log10 of the data ")
fig.update_xaxes(ticktext=[f"{10 ** i}" for i in np.linspace(-6, 6, 13)], tickvals=np.linspace(-6, 6, 13),
                 title="total intrest")
fig.update_yaxes(title="leverage")
fig.show()
