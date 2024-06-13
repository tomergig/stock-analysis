import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.colors import n_colors
from plotly.subplots import make_subplots
from analysis_functions import stats_per_period, probabiliy_losing, get_last
from data_preprocess import sp500_data,sp5003x_data

data_reg = sp500_data()
data3x= sp5003x_data()
data = data3x.join(data_reg,how='inner',lsuffix='_3')
YEARS = 1
INVESTMENT_PERIOD = 365 * YEARS
INTEREST_VALUES = data['interest']
INTEREST_VALUES3x = data['interest_3']


#%%
lose_half,last_value = stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, 1,1,YEARS,probabiliy_losing(0.5), get_last)
lose_half_sim3x,last_value_sim3x =stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, 3,0.97,YEARS, probabiliy_losing(0.5),get_last)
lose_half_3x,last_value_3x = stats_per_period(INTEREST_VALUES3x, INVESTMENT_PERIOD, 1,0.97,YEARS, probabiliy_losing(0.5),get_last)



diff=data['interest_3']-3*data['interest']
# px.histogram(diff).show()

# Displays the distribution of the total interest
# (with a log10 transform) as a function of leverage, the total interest
# the x-axis reflects the true value

colors = n_colors('rgb(5, 0, 200)', 'rgb(200, 10, 10)', 10, colortype='rgb')
fig = go.Figure()
fig.add_trace(go.Violin(x=last_value, spanmode='hard',name='1x'))
fig.add_trace(go.Violin(x=last_value_sim3x, spanmode='hard',name='3x simulation'))
fig.add_trace(go.Violin(x=last_value_3x, spanmode='hard',name='3x'))
fig.update_traces(orientation='h', side='positive', width=3, points=False)
fig.show()




df=pd.DataFrame({"regular":[np.mean(lose_half),np.mean(np.array(last_value) > 1),np.std(np.array(last_value) > 1)],
                 "3x":[np.mean(lose_half_3x),np.mean(np.array(last_value_3x) > 1),np.std(np.array(last_value_3x) > 1)],
                 "3x simulation":[np.mean(lose_half_sim3x),np.mean(np.array(last_value_sim3x) > 1),np.std(np.array(last_value_sim3x) > 1)]}
                ,index=["prob. to lose 50%","prob. profit","std profit"])

print(df)





