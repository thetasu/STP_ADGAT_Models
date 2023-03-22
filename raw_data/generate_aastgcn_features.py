import pandas as pd
import numpy as np
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
##new feature
selected_data["earning rate"] = (selected_data["PRC"] - selected_data["OPENPRC"]) / selected_data["OPENPRC"]
selected_data["BIDLO_rate"] = (selected_data["BIDLO"] - selected_data["OPENPRC"]) / selected_data["OPENPRC"]
selected_data["ASKHI_rate"] = (selected_data["ASKHI"] - selected_data["OPENPRC"]) / selected_data["OPENPRC"]
selected_data["turnover"] = selected_data["VOL"] / selected_data["SHROUT"] / 1000
count = 1
for code,info in selected_data.groupby(by='STOCK_ID'):
    # low, high, open, close, n_close
    low = info['BIDLO'].astype(np.float32).values.tolist()
    high = info['ASKHI'].astype(np.float32).values.tolist()
    open_p = info['OPENPRC'].astype(np.float32).values.tolist()
    close = info['PRC'].astype(np.float32).values.tolist()
    c_low, c_high,c_open,n_close = [None], [None], [None], [None]
    for i in range(1,len(close)):
        c_low.append('%.6f' % (100 * (low[i] / close[i] - 1)))
        c_high.append('%.6f' % (100 * (high[i] / close[i] - 1)))
        c_open.append('%.6f' % (100 * (open_p[i] / close[i] - 1)))
        n_close.append('%.6f' % (100 * (close[i] / close[i-1] - 1)))
    selected_data.loc[selected_data['STOCK_ID'] == code, 'c_low'] = c_low
    selected_data.loc[selected_data['STOCK_ID'] == code, 'c_high'] = c_low
    selected_data.loc[selected_data['STOCK_ID'] == code, 'c_open'] = c_low
    selected_data.loc[selected_data['STOCK_ID'] == code, 'n_close'] = c_low
    # 5_day_close, 10_day_close, 15_day_close, 20_day_close, 25_day_close, 30_day_close
    day = [[None] * 29, [None] * 29, [None] * 29, [None] * 29, [None] * 29, [None] * 29]
    for i in range(29, len(close)):
        for j, T in enumerate([5, 10, 15, 20, 25, 30]):
            day[j].append('%.6f' % (100 * (sum(close[i - T + 1: i + 1]) / T / close[i] - 1)))
    selected_data.loc[selected_data['STOCK_ID'] == code, '5_day_close'] = day[0]
    selected_data.loc[selected_data['STOCK_ID'] == code, '10_day_close'] = day[1]
    selected_data.loc[selected_data['STOCK_ID'] == code, '15_day_close'] = day[2]
    selected_data.loc[selected_data['STOCK_ID'] == code, '20_day_close'] = day[3]
    selected_data.loc[selected_data['STOCK_ID'] == code, '25_day_close'] = day[4]
    selected_data.loc[selected_data['STOCK_ID'] == code, '30_day_close'] = day[5]
    print("Generate Dateset:{} STOCK:{}...".format(count, code))
    count +=1
print('3************************************************3')

print(selected_data)
print('4************************************************4')

stocks = selected_data[selected_data["STOCK_ID"].isin(Selected_Stock)]
# 730 days
# stocks = stocks[stocks['date'] >= '2010/12/27']
# 700 days
stocks = stocks[stocks['date'] >= '2011/02/08']

stocks = stocks[stocks['date'] <= '2013/11/18']
print(stocks)
print('5************************************************5')

Xs = stocks.sort_values(["date","STOCK_ID"])[["c_low","c_high","c_open","n_close","5_day_close","10_day_close","15_day_close","20_day_close","25_day_close","30_day_close"]].values
print('Xs.shape:{}'.format(Xs.shape))

# directly reshape after choose date for aastgcn
# 730 days
# Xs = np.reshape(Xs,[730,198,10])
# 700 days
Xs = np.reshape(Xs,[700,198,10])


print('Xs after reshape:{}'.format(Xs.shape)) # (730,198,5)
print('6************************************************6')

with open('x_numerical_aastgcn_10features_700.pkl','wb') as f:
    pickle.dump(Xs,f)
    f.close()
print('x_numerical_10features save success')
print('7************************************************7')



