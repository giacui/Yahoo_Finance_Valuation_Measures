

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

    return result_df.set_index(0).T


result_df = get_key_stats("T")



###############################################################################
##############Create a Pandas DF for a list of tickers ########################
###############################################################################

tickers=["OMC","WPP","IPG","DNTUF","ACN","IT","HURN","BAH","FCN","PRFT","CTSH","VRTU","FLNT","MCHX","DMS","QUOT","PFSW","THRY","KBNT","MRIN","CREX","BLIN"]
all_result_df = pd.DataFrame()

for ticker in tickers:

    result_df = get_key_stats(ticker)

    if len(all_result_df) ==0:
        all_result_df = result_df
    else:
        all_result_df = all_result_df.append(result_df)

# TO DO ##### Select specific columns (9 columns in "Valuation Measures")#########
# TO DO ##### Change data type, convert B(Billion) and M(Million) to numbers #####
# TO DO ##### Set column names and row indexes #########







###############################################################################
############## Save DF in Excel & format the table ############################
###############################################################################


day=datetime.today().strftime('%Y-%m-%d')
stamp=pd.Timestamp('now').strftime('%B-%d-%Y %I:%M %p')

# TO DO #####  Speciry file direcory #####
#Customize file name
filename = "Yahoo Finance_" + day + ".xlsx"
writer = pd.ExcelWriter(filename, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object; Customize Sheet name and table location
all_result_df.to_excel(writer, sheet_name=day,startrow=3,startcol=1,index=False,header=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book

# Pre-define formatting
bold = workbook.add_format({'bold': True})
cell_format = workbook.add_format()
cell_format.set_align('left')
# TO DO #####  Set the column width and format. #####


# Add date and time stamp
worksheet = writer.sheets[day]
worksheet.write('B1', stamp, bold)

# Add column names
worksheet.write('B3', 'Market Cap', bold)
worksheet.write('C3', 'Enterprise Value', bold)
worksheet.write('D3', 'Trailing P/E', bold)
worksheet.write('E3', 'Forward P/E 1', bold)
worksheet.write('F3', 'PEG Ratio (5 yr expected)', bold)
worksheet.write('G3', 'Price/Sales (ttm)', bold)
worksheet.write('H3', 'Price/Book (mrq)', bold)
worksheet.write('I3', 'Enterprise Value/Revenue', bold)
worksheet.write('J3', 'Enterprise Value/EBITDA', bold)

row_number=3

for ticker in tickers:
    row_number += 1
    cell='A'+str(row_number)
    worksheet.write(cell,ticker, bold)


writer.save()
