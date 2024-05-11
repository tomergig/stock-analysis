# stock-analysis

### stock_leverage.py
This file presents a little analysis of (currently) the sp500 index.
mainly checking investment in the normal manner vs investment in a leveraged index,
aka each daily interest rate is doubled by a leveraging factor.
 
### create_sample_data.py
In addition to this I wanted to explore creating a "sample data" for the index but eventually left this idea
as testing over past data seemed more reliable. nevertheless this trial is shown in the file mentioned 

### data_preprocess.py
currently only for th sp500, In this file are functions to create the raw data from the index\stock data file

### analysis_functions.py
Helper functions to perform the main analysis

### positive_interest_downscaled.py
In this script I toyed with the idea that you can have profit even when downscaleing each positive
interest rate by some factor 