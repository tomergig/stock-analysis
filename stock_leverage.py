
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.colors import n_colors
from plotly.subplots import make_subplots
from analysis_functions import stats_per_period, probabiliy_losing, get_last
from constants import *


# Displays the distribution of the total interest
# (with a log10 transform) as a function of leverage, the total interest
# the x-axis ticks reflects the true value
def ridgeline_final_value():
    colors = n_colors('rgb(5, 0, 200)', 'rgb(200, 10, 10)', 10, colortype='rgb')
    fig = go.Figure()
    leverages = np.arange(1, 8, 0.5)
    for leverage, color in zip(leverages, colors):
        last_value = stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, leverage,
                                      COMMISSION,YEARS,
                                      get_last)[0]
        fig.add_trace(go.Violin(x=np.log10(last_value), line_color=color, name=round(leverage, 3), spanmode='hard',
                                meanline_visible=True))
    fig.update_traces(orientation='h', side='positive', width=3, points=False)
    fig.add_annotation(x=-2, y=1, text="The hover-info is for the log10 of the final value", showarrow=False)
    fig.update_xaxes(ticktext=[f"{10 ** i}" for i in np.linspace(-6, 6, 13)], tickvals=np.linspace(-6, 6, 13),
                     title="final value from 1")
    fig.update_yaxes(title="leverage")
    fig.update_layout(title=" Ridge-line of each final value distribution from investment of 1", title_x=0.5,
                      legend=dict(traceorder='reversed'))
    return fig


# Displays the distribution of the difference from the regular last value
def interest_differance_distribution():
    # None-Leveraged last values
    last_value_regular = np.float16(stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, 1, 1, 1, get_last)[0])

    leverages = np.arange(1, 8, 1)
    fig = make_subplots(cols=1, rows=len(leverages), vertical_spacing=0.03, shared_xaxes='all',shared_yaxes='all')
    colors = n_colors('rgb(100, 255, 100)', 'rgb(255, 100, 100)', len(leverages), colortype='rgb')
    for leverage, color, index in zip(leverages, colors, range(1, len(leverages))):
        last_value = np.float16(stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, leverage,
                                                 COMMISSION if leverage>1 else 1, 1,
                                                 get_last)[0])
        diff_from_norm = (np.array(last_value).reshape(-1, 1) - np.array(last_value_regular).reshape(1, -1)).reshape(-1)
        count, bins = np.histogram(diff_from_norm, bins=np.arange(-5, 5, 0.1))
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        count = count / sum(count)
        fig.add_trace(go.Bar(x=bin_centers, y=count, marker_color=color, name=str(leverage)), col=1, row=index)
        fig.update_yaxes(tick0=0, dtick=round(max(count), 2), col=1, row=index)
        fig.add_vline(x=0, annotation_text=f"P(diff>0) :<b>{np.mean(diff_from_norm > 0):.2f}</b>",
                      annotation_font_color='black', col=1, row=index)
        fig.add_vline(x=min(diff_from_norm)*1.1 , annotation_text=f"<b>min :{min(diff_from_norm):.2f}</b>",
                      annotation_font_color=color, annotation_xanchor='right', col=1, row=index)
        fig.add_vline(x=5*1.1, annotation_text=f"<b> max :{max(diff_from_norm):.2f}</b>",
                      annotation_font_color=color, col=1, row=index)
        fig.update_yaxes(tickvals=np.arange(0,0.4,0.05),col=1, row=index)

    fig.update_layout(title="(normal - leveraged) interest distributions", title_x=0.5, bargap=0,
                      height=100 * len(leverages))
    return fig
#



def profit_loss_stats():
    last_value_regular = np.float16(stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, 1, 1, 1, get_last)[0])
    # Displays the different prob. statistics for different leverages
    leverages = np.arange(1, 6, 0.2)
    data = pd.DataFrame(index=leverages)
    for leverage in leverages:
        binary_lost, last_value = stats_per_period(INTEREST_VALUES, INVESTMENT_PERIOD, leverage,
                                                   COMMISSION, YEARS,
                                                   probabiliy_losing(0.5),get_last)
        last_value = np.array(last_value)
        last_value_regular = np.array(last_value_regular)
        data.at[leverage, 'probability to lose 50%'] = np.mean(binary_lost)
        data.at[leverage, 'probability for profit'] = np.mean(np.array(last_value) > 1)
        diff_from_norm = (last_value.reshape(-1, 1) - last_value_regular.reshape(1, -1)).reshape(-1)
        profit_bool = (last_value > 0) & (last_value_regular > 0)
        diff_from_norm_conditional = (
                last_value[profit_bool].reshape(-1, 1) - last_value_regular[profit_bool].reshape(1, -1)).reshape(-1)
        data.at[leverage, 'probability to profit<br> more then non-leveraged'] = np.mean(diff_from_norm > 0)
        data.at[leverage, 'prob. to earn more given you profited'] = np.mean(diff_from_norm_conditional > 0)

    data['prob. earn more then non-leveraged<br> and profit'] = data['prob. to earn more given you profited'] * data['probability for profit']
    fig = px.line(data)
    fig.add_trace(go.Scatter(x=data.idxmax(), y=data.max(), mode='markers',name="max values", marker=dict(color='red')))
    fig.update_layout(title="Different probability statistics",title_x=0.5,xaxis_title="leverage",yaxis_title="probability")
    return fig

