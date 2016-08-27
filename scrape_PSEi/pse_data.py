#!Users/Jerome/Anaconda3/envs/py27/python
'''
cd '/media/dl/Windows8_OS/Users/Jerome/Google Drive/project/B_finance/fund_invest'
source activate py27
ipython
run pse_data

2016/2/20: scraping and plotting data
2016/8/24: 

see predict_psei.py for predicting future price of stocks.

This is complement of json_scrape.py to get last price history data from each PSE company from bloomberg
url, http://www.bloomberg.com/markets/chart/data/1M/mbt:pm, has outputs data in json
The daily, monthly, or yearly price data of a given list of PSE company is shown in the figure

See scholarship scraper to resolve issue in urlib, skips if data not found, not terminate whole program as in here
'''
#Last Update 2/20:
import urllib
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime as dt
import time
import csv
import glob

datetoday = dt.today().strftime('%Y-%m-%d')

def save_data(filename, i, data):
    file_list = glob.glob('pse_data/new_data/*.json')
    j=0
    ticker_list = []
    for j in range(len(file_list)-1):
	ticker_list.append(file_list[j][18:-7]) #get ticker name only
	j=+1
    ticker_list = list(set(ticker_list)) #remove duplicate 
    if time.upper() == 'D':
	with open(filename[:-6]+datetoday+'.json', 'w') as outfile:
            json.dump(data, outfile)
	    print 'created %s_%s.json' %(i, datetoday)
    else: #i not in ticker_list, then save as
	with open(filename, 'w') as outfile:
                json.dump(data, outfile)
	print 'created %s.json' %i
    
    #print 'Obtained data of (%d) companies:\n %s' %(len(ticker_list),ticker_list)
    return data

#list of symbols/tickers of companies registered in PSE
#symlist = ['I','LOTO','FGEN','MFIN','NOW','SRDC','PERC','FOOD','COL','MPI','AP','NRCP','YEHEY','VLL','PNX','PIP','ALHI','SPH','ORE','EIBB','RWM','ANI','HOUSE','H2O','ALT','NIKL','ROCK','CPM','IMI','EG','MWIDE','DMW','PXP','PGOLD','TECH','EMP','GTCAP','DNL','CAL','COAL','PBB','DMPL','TUGS','AGF','DWC','TFHI','RRHI','CIC','DD','CNPF','TAPET','SSI','PSPC','PGI','X','CROWN','SBS','DATEM','MRSGI','IDC','MER','TEL','EEI','FPH','COSCO','PNB','ICT','HI','PX','KEP','KPH','KPHB','POPI','RLT','MACAY','ANS','ABA','AR','ABS','ACE','MARC','ABG','APO','APX','AT','LR','AB','AC','ALI','PHN','PAL','BPI','BSC','BEL','BC','BCB','BMM','CPV','CPVB','RCI','BCOR','CAT','CEU','CIP','CHIB','CA','CAB','BH','DIZ','ECP','FEU','PAX','FDC','FLI','FYN','FYNB','CYBR','GLO','GPH','IMP','IMPB','MAC','ARA','MCP','IRC','IS','ISM','ATN','ATNB','STI','JGS','JFC','ZHI','GEO','PORT','LC','LFM','PHC','LIHC','MHC','LCB','MBC','MB','MJC','MA','MAB','LTG','SGP','DAVIN','MAH','MAHB','MCB','PMPC','MBT','MED','CPG','OM','OPM','OPMB','JAS','PA','MJIC','V','PCP','IPO','TFC','PBC','PHES','OV','PRC','PTT','PTC','STR','PRIM','PPC','MG','PF','SUN','LRI','REG','WIN','RFM','RCB','RLC','MGH','SMC','SPM','SHNG','WEB','STN','NI','GO','GOB','ACR','TA','FJP','FJPB','UBP','UPM','SGI','EIBA','VUL','SLI','LPZ','SOC','VMC','PCOR','UNI','URC','MEG','SMPH','VVT','PSB','LIB','APC','CEI','CDC','CHI','SFI','AEV','FAF','FNI','SCC','BKR','FPI','VITA','WPI','2GO','GSMI','MRC','PNC','SECB','ION','PLC','LMG','BRN','ELI','LSC','PMT','ATI','DMC','GERI','AAA','HLCM','EVER','UW','ALCO','GREEN','NXGEN','ROX','MVC','BHI','PHA','SLF','BLFI','SM','EDC','SEVN','IPM','EURO','LAND','AUB','AGI','GMA7','MWC','EW','MFC','PSE','BLOOM','BDO','DFNN','CEB','MAXS','CSB','PRMX','T','TBGI','LBC','JOH','SPC']

symlist = ['VITA','MBT','FGEN','BDO','SMPH']

time = raw_input('Print history format: yearly (Y), monthly (M), daily (D)\n')
response = raw_input('Show plots? Yes (y) or No (n) \n')

if time.upper() == 'Y':
    print 'Obtaining yearly data'
    xfmt = mdates.DateFormatter('%m-%d-%Y')
elif time.upper() == 'M':
    print 'Obtaining monthly data'
    xfmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
elif time.upper() == 'D':
    print 'Obtaining daily data'
    xfmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
else:
    print 'Unknown input. Please run again.'

unixdate_array = []
date_array = []
price_array = []
date_price_array = []

try: #while i < len(symlist):
    for i in symlist:
	filename = 'pse_data/new_data/'+str(i)+'_'+time.upper()+'.json'
        url = "http://www.bloomberg.com/markets/chart/data/1"+time.upper()+"/"+i+":PM" #depends on input time format
        htmltxt = urllib.urlopen(url)
        data = json.load(htmltxt)           #json constructs an easily accessible data structure      
        datapoints = data["data_values"]    #last price data of a given company
        print '1 %s data for %s' %(time.upper(), i)
	###PARSE date and price data         
	for point in datapoints:
            #date_array.append(point[0] / 1e3) #since json is a tuple, [0] is the timestamp and [1] is the price value
            unixdate_array.append(point[0] / 1e3)
            date_array.append(dt.fromtimestamp(point[0] / 1e3)) # 1e3 to remove milli sec 
            price_array.append(point[1])
            pair = str(point[0])+','+str(point[1])+'\n'
            date_price_array.append(pair)
	###1D data consists of additional parameters
        if time.upper() == 'D':
            close_price = data["prev_close"]
            close_time = str(dt.fromtimestamp(data["exch_close_time"]/1e3))
            print 'prev_close: ', close_price
            print 'exch_open_time: ', str(dt.fromtimestamp(data["exch_open_time"]/1e3))
            print 'exch_close_time: ', close_time
	if response.lower() == ('y' or 'yes'):     #skip if FALSE       
		plt.subplots_adjust(bottom=0.2)
		plt.xticks(rotation=25)
		ax=plt.gca()
		ax.xaxis.set_major_formatter(xfmt)
		ax.grid(True)
		plt.plot(date_array,price_array)
		plt.title('%s has n=%d datapoints' %(i,len(datapoints)))
		plt.ylabel('Price')
		plt.show()
        	print '%s has n=%d data points' %(i,len(datapoints))
		#SAVE
		save_data(filename, i, data)
	elif response.lower() == ('n' or 'no'): 
		save_data(filename, i, data)
        date_array = []
        price_array = [] #clear before appended by new data
        #raw_input('next')
except Exception,e:
    print 'failed in the main loop due to: ', str(e)
