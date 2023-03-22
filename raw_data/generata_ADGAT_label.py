import numpy as np
import pandas as pd
import pickle


Selected_Stock = ['NYSE:AAP', 'NYSE:ABC', 'NYSE:ABT', 'NYSE:ADM', 'NYSE:ADS',
'NYSE:AEP', 'NYSE:AES', 'NYSE:AET', 'NYSE:AFL', 'NYSE:AGN',
'NYSE:AIG', 'NYSE:ALK', 'NYSE:ALL', 'NYSE:AMD', 'NYSE:AMP',
'NYSE:APA', 'NYSE:APC', 'NYSE:AXP', 'NYSE:BA', 'NYSE:BAC',
'NYSE:BAX', 'NYSE:BBT', 'NYSE:BBY', 'NYSE:BEN', 'NYSE:BK',
'NYSE:BLK', 'NYSE:BLL', 'NYSE:BMY', 'NYSE:BSX', 'NYSE:CAG',
'NYSE:CAT', 'NYSE:CB', 'NYSE:CBG', 'NYSE:CF', 'NYSE:CHK',
'NYSE:CI', 'NYSE:CL', 'NYSE:CMA', 'NYSE:CMI', 'NYSE:CMS',
'NYSE:COF', 'NYSE:COO', 'NYSE:COP', 'NYSE:CPB', 'NYSE:CRM',
'NYSE:CSX', 'NYSE:CVS', 'NYSE:CVX', 'NYSE:DE', 'NYSE:DIS',
'NYSE:DTE', 'NYSE:DUK', 'NYSE:ED', 'NYSE:EIX', 'NYSE:EL',
'NYSE:EMN', 'NYSE:EMR', 'NYSE:EQT', 'NYSE:ETR', 'NYSE:EXC',
'NYSE:F', 'NYSE:FCX', 'NYSE:FDX', 'NYSE:FE', 'NYSE:FL', 'NYSE:GD',
'NYSE:GE', 'NYSE:GIS', 'NYSE:GPS', 'NYSE:GS', 'NYSE:HAL',
'NYSE:HD', 'NYSE:HES', 'NYSE:HIG', 'NYSE:HOG', 'NYSE:HON',
'NYSE:HP', 'NYSE:HPQ', 'NYSE:HUM', 'NYSE:IBM', 'NYSE:ICE',
'NYSE:IP', 'NYSE:IT', 'NYSE:JCI', 'NYSE:JNJ', 'NYSE:JPM',
'NYSE:JWN', 'NYSE:K', 'NYSE:KEY', 'NYSE:KMB', 'NYSE:KO', 'NYSE:KR',
'NYSE:LEG', 'NYSE:LLY', 'NYSE:LMT', 'NYSE:LOW', 'NYSE:LUK',
'NYSE:LUV', 'NYSE:MA', 'NYSE:MAS', 'NYSE:MCD', 'NYSE:MCO',
'NYSE:MDT', 'NYSE:MET', 'NYSE:MGM', 'NYSE:MMM', 'NYSE:MO',
'NYSE:MON', 'NYSE:MOS', 'NYSE:MRK', 'NYSE:MRO', 'NYSE:MS',
'NYSE:NBL', 'NYSE:NEM', 'NYSE:NI', 'NYSE:NKE', 'NYSE:NOC',
'NYSE:NOV', 'NYSE:NRG', 'NYSE:NUE', 'NYSE:OXY', 'NYSE:PCG',
'NYSE:PEG', 'NYSE:PEP', 'NYSE:PFE', 'NYSE:PFG', 'NYSE:PG',
'NYSE:PGR', 'NYSE:PH', 'NYSE:PHM', 'NYSE:PNC', 'NYSE:PRU',
'NYSE:PX', 'NYSE:RF', 'NYSE:RJF', 'NYSE:RL', 'NYSE:RTN',
'NYSE:SEE', 'NYSE:SJM', 'NYSE:SO', 'NYSE:SRE', 'NYSE:STI',
'NYSE:STT', 'NYSE:T', 'NYSE:TGT', 'NYSE:TIF', 'NYSE:TSN',
'NYSE:TWX', 'NYSE:TXT', 'NYSE:UNH', 'NYSE:UNP', 'NYSE:UPS',
'NYSE:USB', 'NYSE:UTX', 'NYSE:VLO', 'NYSE:VZ', 'NYSE:WFC',
'NYSE:WHR', 'NYSE:WMB', 'NYSE:WMT', 'NYSE:WU', 'NYSE:WYN',
'NYSE:XOM', 'NYSE:XRX', 'NYSE:YUM', 'NasdaqGS:AAPL',
'NasdaqGS:ADBE', 'NasdaqGS:ALGN', 'NasdaqGS:AMAT', 'NasdaqGS:AMGN',
'NasdaqGS:AMZN', 'NasdaqGS:ATVI', 'NasdaqGS:BIIB',
'NasdaqGS:CMCSA', 'NasdaqGS:COST', 'NasdaqGS:CSCO',
'NasdaqGS:CTSH', 'NasdaqGS:DISH', 'NasdaqGS:EBAY', 'NasdaqGS:ESRX',
'NasdaqGS:EXPE', 'NasdaqGS:FAST', 'NasdaqGS:GILD', 'NasdaqGS:GOOG',
'NasdaqGS:INTC', 'NasdaqGS:INTU', 'NasdaqGS:MSFT', 'NasdaqGS:NDAQ',
'NasdaqGS:NFLX', 'NasdaqGS:NTRS', 'NasdaqGS:NVDA', 'NasdaqGS:QCOM',
'NasdaqGS:SBUX', 'NasdaqGS:SYMC', 'NasdaqGS:TROW', 'NasdaqGS:TSCO',
'NasdaqGS:WYNN', 'NasdaqGS:XRAY']
Selected_Stock = [x.replace("NYSE:","1") for x in Selected_Stock]
Selected_Stock = [x.replace("NasdaqGS:","3") for x in Selected_Stock]
Selected_Stock = set(Selected_Stock)
print(Selected_Stock)
stock_data = pd.read_csv("market_data.csv",skipinitialspace=True)
print(len(Selected_Stock))
#filter by database rules
stock_data = stock_data[stock_data["SHRCD"] == 11]
stock_data = stock_data[stock_data["EXCHCD"].isin([1,2,3])]
stock_data = stock_data[stock_data["TRDSTAT"] == "A"]
#filter by missing values
stock_data =  stock_data[-pd.isna(stock_data["BIDLO"])]
stock_data =  stock_data[-pd.isna(stock_data["ASKHI"])]
stock_data =  stock_data[-pd.isna(stock_data["PRC"])]
stock_data =  stock_data[-pd.isna(stock_data["VOL"])]
stock_data =  stock_data[-pd.isna(stock_data["SHROUT"])]
stock_data =  stock_data[-pd.isna(stock_data["OPENPRC"])]
#unique_id = exchcd + ticker
stock_data["STOCK_ID"] = stock_data["EXCHCD"].astype(int).astype(str) + stock_data["TICKER"]
print(stock_data)
print('1************************************************1')
#filter by complete trascation record
full_time = len(stock_data["date"].unique())
count_stock_trans = stock_data.groupby("STOCK_ID").count()
selected = count_stock_trans[count_stock_trans["date"] == full_time].index
selected_data  = stock_data[stock_data["STOCK_ID"].isin(selected)]
selected_data = selected_data.sort_values(["STOCK_ID","date"]).reset_index(drop = True)
print(selected_data)
print('2************************************************2')

# for ADGAT
selected_data = selected_data[selected_data['date'] >= '2010/12/27'] # rnn_length=30
# for aastgcn
# selected_data = selected_data[selected_data['date'] >= '2011/02/08']

selected_data = selected_data[selected_data['date'] <= '2013/11/19']
selected_data = selected_data[selected_data["STOCK_ID"].isin(Selected_Stock)]

Close_price = selected_data.sort_values(["date","STOCK_ID"])[["PRC"]].values
print('Close_price.shape:{}'.format(Close_price.shape))
# for ADGAT
Close_price = np.reshape(Close_price,[731,198])
# for aastgcn
# Close_price = np.reshape(Close_price,[701,198])
label_matrix = np.zeros([Close_price.shape[0]-1, Close_price.shape[1]])
for index in range(label_matrix.shape[1]):
    for col in range(label_matrix.shape[0]-1):
        temp = Close_price[col+1][index] - Close_price[col][index]
        label_matrix[col][index] = temp
print('label_matrix.shape:{}'.format(label_matrix.shape))
print(label_matrix)

with open('close_y_ADGAT_730.pkl','wb') as f:
    pickle.dump(label_matrix,f)
    f.close()
print('close_y save success')
print('10************************************************10')

# ##new feature
# selected_data["earning rate"] = (selected_data["PRC"] - selected_data["OPENPRC"]) / selected_data["OPENPRC"]
# selected_data["BIDLO_rate"] = (selected_data["BIDLO"] - selected_data["OPENPRC"]) / selected_data["OPENPRC"]
# selected_data["ASKHI_rate"] = (selected_data["ASKHI"] - selected_data["OPENPRC"]) / selected_data["OPENPRC"]
# selected_data["turnover"] = selected_data["VOL"] / selected_data["SHROUT"] / 1000
# ##shift earning rate y earning_rate_tmr
# ##shift opening price
# grouped = selected_data.groupby("STOCK_ID")
# selected_data["earning_rate_tmr"] = grouped["earning rate"].transform(shift_col,False)
# selected_data["PRC_yes"] = grouped["PRC"].transform(shift_col,True)
# selected_data["open_rate"] = (selected_data["OPENPRC"] - selected_data["PRC_yes"]) / selected_data["PRC_yes"]
# selected_data["open_rate_tmr"] = grouped["open_rate"].transform(shift_col,False)
# ##delete the last call
# selected_data = selected_data.groupby(["STOCK_ID"], group_keys=False).apply(lambda x: x.iloc[:-1])
# selected_data.reset_index(drop = True, inplace=True)
# print(selected_data)
# print('3************************************************3')
# ##normalize
# selected_data["BIDLO_rate"] = grouped["BIDLO_rate"].transform(normalize_col)
# selected_data["ASKHI_rate"] = grouped["ASKHI_rate"].transform(normalize_col)
# selected_data["turnover"] = grouped["turnover"].transform(normalize_col)
# selected_data["earning rate"] = grouped["earning rate"].transform(normalize_col)
# selected_data["open_rate_tmr"] = grouped["open_rate_tmr"].transform(normalize_col)
# print(selected_data)
# print('4************************************************4')
#
# ##Align with news
# stocks = selected_data.groupby(["STOCK_ID"], group_keys=False).apply(lambda x: x.iloc[14:])
# stocks = stocks.groupby(["STOCK_ID"], group_keys=False).apply(lambda x: x.iloc[:-28])
# stocks = stocks[stocks["STOCK_ID"].isin(Selected_Stock)]
# print(stocks)
# print('5************************************************5')
#
# # filter with data set range 700+rnn_length
# # stocks = stocks[stocks['date'] >= '2011/02/08']
# stocks = stocks[stocks['date'] >= '2010/12/27'] # rnn_length=30
# stocks = stocks[stocks['date'] <= '2013/11/18']
# print(stocks)
# print('6************************************************6')
#
# Xs = stocks.sort_values(["date","STOCK_ID"])[["BIDLO_rate","ASKHI_rate","turnover","earning rate","open_rate_tmr"]].values
# Ys = stocks.sort_values(["date","STOCK_ID"])[["earning_rate_tmr"]].values
# Close_price = stocks.sort_values(["date","STOCK_ID"])[["PRC"]].values
# print('Xs before reshape:{}'.format(Xs.shape)) # (138600,5)
# print('Ys before reshape:{}'.format(Ys.shape)) # (138600,1)
# print('Close_price before reshape:{}'.format(Close_price.shape)) # (138600,1)
# print('7************************************************7')
#
# # directly reshape after choose date
# Xs = np.reshape(Xs,[730,198,5])
# Ys = np.reshape(Ys,[730,198])
# Close_price = np.reshape(Close_price,[730,198])
# print('Xs after reshape:{}'.format(Xs.shape)) # (730,198,5)
# print('Ys after reshape:{}'.format(Ys.shape)) # (730,198)
# print('Close_price after reshape:{}'.format(Close_price.shape)) # (730,198)
# print('8************************************************8')