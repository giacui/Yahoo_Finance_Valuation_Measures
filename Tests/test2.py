import pandas as pd
from yahoofinancials import YahooFinancials


def get_stats_df_1(ticker):
    yahoo_financials = YahooFinancials(ticker)
    statistics=yahoo_financials.get_key_statistics_data()
    stats_df_1=pd.DataFrame(statistics).loc[['enterpriseValue'],:].transpose()
    stats_df_1['marketCap']= [yahoo_financials.get_market_cap()]

    return stats_df_1

tickers=["OMC","WPP","IPG","DNTUF","ACN","IT","HURN","BAH","FCN","PRFT","CTSH","VRTU","FLNT","MCHX","DMS","QUOT","PFSW","THRY","KBNT","MRIN","CREX","BLIN"]
all_df_1 = pd.DataFrame()

for ticker in tickers:

    stats_df_1 = get_stats_df_1(ticker)

    if len(all_df_1) ==0:
        all_df_1 = stats_df_1
    else:
        all_df_1 = all_df_1.append(stats_df_1)

print(all_df_1)
       
