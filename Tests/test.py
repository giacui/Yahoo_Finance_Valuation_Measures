

import pandas as pd
import requests
import bs4 as bs
import xlsxwriter
from datetime import datetime

###############################################################################
########Function to scrape data from yahoo finance statistics page ############
###############################################################################

def get_key_stats(ticker):

    url = r'https://sg.finance.yahoo.com/quote/{0}/key-statistics?p={0}'.format(ticker)

    # Fake as a browser, otherwise Yahoo will block you
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    df_list = pd.read_html(requests.get(url, headers=headers).text)
    result_df = df_list[0]
    for df in df_list[1:]:
        result_df = result_df.append(df)
    valuation_measures=result_df[0:9].set_index(0).T

    return valuation_measures


###############################################################################
##############Create a Pandas DF for a list of tickers ########################
###############################################################################

tickers=["OMC","WPP"]
all_result_df = pd.DataFrame()

for ticker in tickers:

    valuation_measures = get_key_stats(ticker)

    if len(all_result_df) ==0:
        all_result_df = valuation_measures
    else:
        all_result_df = all_result_df.append(valuation_measures)


print(all_result_df)
