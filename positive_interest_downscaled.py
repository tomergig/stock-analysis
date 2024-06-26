import plotly.express as px
import pandas as pd
import numpy as np
from data_preprocess import sp500_data

from constants import *


data = sp500_data()
up = data[data['interest'] > 0]['interest']
down = data[data['interest'] < 0]['interest']
downscaleing_values=np.linspace(0.85, 1, 100)
df= pd.DataFrame(index=downscaleing_values)
for leverage in [1,2,3,4,5,6]:
    for downscale in downscaleing_values:
        final_value=[]
        for _ in range(REPETITIONS):
            random_positive_interest = np.random.choice(up, size=round(INVESTMENT_PERIOD * (len(up) / len(data))), replace=True) * leverage * downscale
            random_negative_interest = np.random.choice(down, size=round(INVESTMENT_PERIOD * (len(down) / len(data))), replace=True) * leverage
            interests = np.concatenate(([1],random_positive_interest+1, random_negative_interest+1))
            final_value.append(np.cumprod(interests)[-1])
        df.at[downscale, f"leverage : {leverage}"]= np.sum(np.array(final_value) > 1) / REPETITIONS


positive_interest_downscaled=px.line(df,labels={'index':'positive interest downscale','value':'probability for profit'}).add_hline(y=0.5,annotation_text= "0.5")
