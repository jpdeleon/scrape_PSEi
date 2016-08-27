#!Users/Jerome/Anaconda3/envs/py27/python
'''
cd '../../media/dl/Windows8_OS/Users/Jerome/Google Drive/project/B_finance/fund_invest'
source activate py27
ipython
run predict_psei.py

This aims to predict the price of a given company/ticker using forecast_out days from the past. The longer the forecast_out days, the higher the error. The label column is shifted forecast_out days into the past and 

2016/8/24: added machine learning: regression

tweakable parameters:
1. time to D, M, or Y
2. n for the number of days or hours of prediction
3. ticker to any of the companies saved as .json 

To do: 
1. fix the problem in missing datapoint between predicted and actual data
2. add time resolution in which prediction can be done arbitrarily (depends on data)
3. predict into the future
4. fix length of prediction into the future
5. loop all tickers in symlist

see pse_data.py for scraping, saving, and plotting of ticker data
'''

import pandas as pd
import json
import numpy as np
from datetime import datetime as dt
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
#%matplotlib inline
style.use('ggplot')
#style.use('fivethirtyeight')

time = 'D'
datetoday = '2016-08-26'
#datetoday = dt.today().strftime('%Y-%m-%d')
ticker='VITA'

#symlist = ['I','LOTO','FGEN','MFIN','NOW','SRDC','PERC','FOOD','COL','MPI','AP','NRCP','YEHEY','VLL','PNX','PIP','ALHI','SPH','ORE','EIBB','RWM','ANI','HOUSE','H2O','ALT','NIKL','ROCK','CPM','IMI','EG','MWIDE','DMW','PXP','PGOLD','TECH','EMP','GTCAP','DNL','CAL','COAL','PBB','DMPL','TUGS','AGF','DWC','TFHI','RRHI','CIC','DD','CNPF','TAPET','SSI','PSPC','PGI','X','CROWN','SBS','DATEM','MRSGI','IDC','MER','TEL','EEI','FPH','COSCO','PNB','ICT','HI','PX','KEP','KPH','KPHB','POPI','RLT','MACAY','ANS','ABA','AR','ABS','ACE','MARC','ABG','APO','APX','AT','LR','AB','AC','ALI','PHN','PAL','BPI','BSC','BEL','BC','BCB','BMM','CPV','CPVB','RCI','BCOR','CAT','CEU','CIP','CHIB','CA','CAB','BH','DIZ','ECP','FEU','PAX','FDC','FLI','FYN','FYNB','CYBR','GLO','GPH','IMP','IMPB','MAC','ARA','MCP','IRC','IS','ISM','ATN','ATNB','STI','JGS','JFC','ZHI','GEO','PORT','LC','LFM','PHC','LIHC','MHC','LCB','MBC','MB','MJC','MA','MAB','LTG','SGP','DAVIN','MAH','MAHB','MCB','PMPC','MBT','MED','CPG','OM','OPM','OPMB','JAS','PA','MJIC','V','PCP','IPO','TFC','PBC','PHES','OV','PRC','PTT','PTC','STR','PRIM','PPC','MG','PF','SUN','LRI','REG','WIN','RFM','RCB','RLC','MGH','SMC','SPM','SHNG','WEB','STN','NI','GO','GOB','ACR','TA','FJP','FJPB','UBP','UPM','SGI','EIBA','VUL','SLI','LPZ','SOC','VMC','PCOR','UNI','URC','MEG','SMPH','VVT','PSB','LIB','APC','CEI','CDC','CHI','SFI','AEV','FAF','FNI','SCC','BKR','FPI','VITA','WPI','2GO','GSMI','MRC','PNC','SECB','ION','PLC','LMG','BRN','ELI','LSC','PMT','ATI','DMC','GERI','AAA','HLCM','EVER','UW','ALCO','GREEN','NXGEN','ROX','MVC','BHI','PHA','SLF','BLFI','SM','EDC','SEVN','IPM','EURO','LAND','AUB','AGI','GMA7','MWC','EW','MFC','PSE','BLOOM','BDO','DFNN','CEB','MAXS','CSB','PRMX','T','TBGI','LBC','JOH','SPC']

symlist = ['VITA','MBT','FGEN','BDO','SMPH']

response = raw_input('Show plots? Yes (y) or No (n) \n')

if time.upper() == 'Y':
    #print 'Obtaining yearly data'
    filename = 'pse_data/new_data/'+ticker+'_Y.json'
    date_format = '%Y-%m-%d'
    offset= 60*60*24 #one day in sec
    #xfmt = mdates.DateFormatter('%m-%d-%Y')
elif time.upper() == 'M':
    #print 'Obtaining monthly data'
    filename = 'pse_data/new_data/'+ticker+'_M.json'
    date_format = '%Y-%m-%d'
    offset= 60*60*24 #one day in sec
    #xfmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
elif time.upper() == 'D':
    #print 'Obtaining daily data'
    filename = 'pse_data/new_data/'+ticker+'_'+datetoday+'.json'
    date_format = '%Y-%m-%d %H:%M:%S'
    offset= 60 #one min in sec
    #xfmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
else:
    print 'Unknown input. Please run again.'

with open(filename, 'r') as fp:
    data = pd.read_json(fp)

#print data.head()    
#print data.columns

unixdate_array = []
date_array = []
price_array = []
date_price_array = []

datapoints = data['data_values']
for point in datapoints:
    date_array.append(point[0] / 1e3) #since json is a tuple, [0] is the timestamp and [1] is the price value
    unixdate_array.append(point[0] / 1e3)
    date_array.append(dt.fromtimestamp(point[0] / 1e3)) # 1e3 to remove milli sec 
    price_array.append(point[1])
    pair = str(point[0])+','+str(point[1])+'\n'
    date_price_array.append(pair)

#convert from unix date to regular date, with dtype=datetime64 
regular_date_array = []
for i in range(len(unixdate_array)):
    regular_date_array.append(np.datetime64(dt.fromtimestamp(unixdate_array[i]).strftime(date_format)))

df1 = pd.Series(price_array, index=regular_date_array)
'''
###quick visualization
df1.plot(grid=True)
plt.title('%s has n=%d datapoints' %(ticker,len(datapoints)))
plt.ylabel('Price')
plt.show()
'''
###create dataframe
d = {'price' : pd.Series(price_array, index=regular_date_array)}
df2 = pd.DataFrame(d)

###create new column based on price data adjusted n-days into the future
forecast_col = 'price'
df2.fillna(-99999, inplace=True)
n=0.05*len(df2)
forecast_out = int(math.ceil(n)) #in days

###create new column for label
df2['label'] = df2[forecast_col].shift(-forecast_out)

#print df2.tail() #Note that the last Forecast has NaN entry

###############################Regression###############################
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

##get just price data
X = np.array(df2.drop(['label'],1)) #drops label and date index
##normalize the datapoints
X = preprocessing.scale(X)
X_lately= X[-forecast_out:] #most recent data (e.g. 95-100)
X = X[:-forecast_out] #data until beginning of X_lately (e.g. 0-94)
#print(X, len(X))

df2.dropna(inplace=True)
y = np.array(df2['label'])
#print(len(X)==len(y))

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#algorithm classification 
clf = LinearRegression(n_jobs=-1) #-1 = efficient/adaptive threading enabled
clf.fit(X_train, y_train)

accuracy = clf.score(X_test,y_test)
print('accuracy is %f' %accuracy)

forecast_set= clf.predict(X_lately)
#print(forecast_set, accuracy, forecast_out)

###add forecast column for predicted values n-days into the future
df2['Forecast'] = np.nan #fill up with nan temporarily

#last_unix=df2.iloc[-1].name
##get the last date offset forecast days into the past
last_unix=unixdate_array[-forecast_out-1]  
##off set one day after
next_unix= last_unix + offset #next day

###PARSE x-axis into date format
for i in forecast_set:
    next_date = dt.fromtimestamp(next_unix)
    next_unix += offset
    df2.loc[next_date] = [np.nan for _ in range(len(df2.columns)-1)] + [i]    

print(df2.tail())

if response.lower() == ('y' or 'yes'):     #skip if FALSE       
	plt.figure(1)
	df2['price'].plot(linewidth=2)
	df2['Forecast'].plot(linewidth=2)
	plt.legend(loc=2) #bottom right
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.show()
