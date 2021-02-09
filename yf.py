

import pandas as pd
from datetime import datetime
from yahoofinancials import YahooFinancials


tickers=["OMC","WPP","IPG","DNTUF","ACN","IT","HURN","BAH","FCN","PRFT","CTSH","VRTU","FLNT","MCHX","DMS","QUOT","PFSW","THRY","KBNT","MRIN","CREX","BLIN"]

for ticker in tickers:

    yahoo_financials = YahooFinancials(ticker)

    print(yahoo_financials.get_key_statistics_data())
