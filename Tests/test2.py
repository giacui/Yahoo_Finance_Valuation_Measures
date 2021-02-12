import pandas as pd
from yahoofinancials import YahooFinancials
import requests
import bs4 as bs
import xlsxwriter
from datetime import datetime


tickers=["OMC","WPP","IPG","DNTUF","ACN","IT","HURN","BAH","FCN","PRFT","CTSH","VRTU","FLNT","MCHX","DMS","QUOT","PFSW","THRY","KBNT","MRIN","CREX","BLIN"]
all_df_1 = pd.DataFrame()
all_df_2 = pd.DataFrame()



def get_df_1(ticker):
    yahoo_financials = YahooFinancials(ticker)
    stats_1=yahoo_financials.get_key_statistics_data()
    df_1=pd.DataFrame(stats_1).loc[['enterpriseValue'],:].transpose()
    df_1['marketCap']= [yahoo_financials.get_market_cap()]

    return df_1

for ticker in tickers:
    df_1 = get_df_1(ticker)
    if len(all_df_1) ==0:
        all_df_1 = df_1
    else:
        all_df_1 = all_df_1.append(df_1)




def get_df_2(ticker):
    url = r'https://sg.finance.yahoo.com/quote/{0}/key-statistics?p={0}'.format(ticker)
    # Fake as a browser, otherwise Yahoo will block you
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    statistics_2 = pd.read_html(requests.get(url, headers=headers).text)
    vMeasures = stats_2 [0]
    for df in stats_2 [1:]:
        vMeasures = vMeasures.append(df)
    df_2=vMeasures[2:9].set_index(0).T

    return df_2

for ticker in tickers:
    df_2 = get_df_2(ticker)
    if len(all_df_2) ==0:
        all_df_2 = df_2
    else:
        all_df_2 = all_df_2.append(df_2)



result = pd.concat([all_df_1, all_df_2], axis=1)
print(result)
