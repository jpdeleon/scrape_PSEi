#!Users/Jerome/Anaconda3/envs/py27/python
#2016/2/19
#cd ../../Google Drive/project/B_finance/fund_invest
'''
first time to use json to scrape single last price data from each company from bloomberg
if url is accessed, it will display a string of values
{"ticker":"MBT:PM","return_code":0,"ttl":300,"disp_name":"Metropolitan Bank & Trust Co","last_price":79.05,"price_precision":4.0,"time_of_last_updt":"2016-02-19","pct_chge_1D":-0.56603801}
json easily scans the text above and then accessed in a format similar to array e.g. data["last_price"] but actually uses a key inside the ""
'''
#see pse_data.py for extension
#Last Update 2/20: I realized I can save daily data into a dictionary or export to a txt file so I can make a time series after running this script and fetching new data daily
#see project/B_finance/fund_invest/pse_data/ for data
import urllib
import re
import json

symlist = ['I','LOTO','FGEN','MFIN','NOW','SRDC','PERC','FOOD','COL','MPI','AP','NRCP','YEHEY','VLL','PNX','PIP','ALHI','SPH','ORE','EIBB','RWM','ANI','HOUSE','H2O','ALT','NIKL','ROCK','CPM','IMI','EG','MWIDE','DMW','PXP','PGOLD','TECH','EMP','GTCAP','DNL','CAL','COAL','PBB','DMPL','TUGS','AGF','DWC','TFHI','RRHI','CIC','DD','CNPF','TAPET','SSI','PSPC','PGI','X','CROWN','SBS','DATEM','MRSGI','IDC','MER','TEL','EEI','FPH','COSCO','PNB','ICT','HI','PX','KEP','KPH','KPHB','POPI','RLT','MACAY','ANS','ABA','AR','ABS','ACE','MARC','ABG','APO','APX','AT','LR','AB','AC','ALI','PHN','PAL','BPI','BSC','BEL','BC','BCB','BMM','CPV','CPVB','RCI','BCOR','CAT','CEU','CIP','CHIB','CA','CAB','BH','DIZ','ECP','FEU','PAX','FDC','FLI','FYN','FYNB','CYBR','GLO','GPH','IMP','IMPB','MAC','ARA','MCP','IRC','IS','ISM','ATN','ATNB','STI','JGS','JFC','ZHI','GEO','PORT','LC','LFM','PHC','LIHC','MHC','LCB','MBC','MB','MJC','MA','MAB','LTG','SGP','DAVIN','MAH','MAHB','MCB','PMPC','MBT','MED','CPG','OM','OPM','OPMB','JAS','PA','MJIC','V','PCP','IPO','TFC','PBC','PHES','OV','PRC','PTT','PTC','STR','PRIM','PPC','MG','PF','SUN','LRI','REG','WIN','RFM','RCB','RLC','MGH','SMC','SPM','SHNG','WEB','STN','NI','GO','GOB','ACR','TA','FJP','FJPB','UBP','UPM','SGI','EIBA','VUL','SLI','LPZ','SOC','VMC','PCOR','UNI','URC','MEG','SMPH','VVT','PSB','LIB','APC','CEI','CDC','CHI','SFI','AEV','FAF','FNI','SCC','BKR','FPI','VITA','WPI','2GO','GSMI','MRC','PNC','SECB','ION','PLC','LMG','BRN','ELI','LSC','PMT','ATI','DMC','GERI','AAA','HLCM','EVER','UW','ALCO','GREEN','NXGEN','ROX','MVC','BHI','PHA','SLF','BLFI','SM','EDC','SEVN','IPM','EURO','LAND','AUB','AGI','GMA7','MWC','EW','MFC','PSE','BLOOM','BDO','DFNN','CEB','MAXS','CSB','PRMX','T','TBGI','LBC','JOH','SPC']

i = 0
try:
    while i < len(symlist):
        url = "http://www.bloomberg.com/markets/watchlist/recent-ticker/"+symlist[i]+":PM"
        htmltext = urllib.urlopen(url)
        data = json.load(htmltext)
        price = data["last_price"]
        update = data["time_of_last_updt"]
        pct_change = data["pct_chge_1D"]
        print data["disp_name"] #works like an array, but "disp_name" is not an index but a json key
        print "last price: ", price
        print "update: ", update
        print "%change:", pct_change
        print '--------------------'
        filename = 'pse_data/'+str(symlist[i])+'.txt'
        data_export = str(update)+','+str(price)+','+str(pct_change)
        with open(filename, "w+") as file:
            data_import = [l.rstrip("\n") for l in file.readlines()] #transform data into array
        with open(filename, "a+") as file:        
            if str(update) not in data_import: #check for duplication
                data_import.append(data_export)                
                file.write(data_export + '\n')
        i+= 1
        
except Exception,e:
    print 'failed in the main loop',str(e)