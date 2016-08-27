'''
Shows a chart of US stock companies with data from yahoo and quandl
'''
#quandl access does not work
#last edited: 2016/2/21
import time
import urllib2
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np

ofInterest = ['AAN', 'ANF', 'ANCX', 'ACE', 'ATVI', 'AET', 'AGCO', 'ATSG', 'AWH', 'ALL', 'AFAM', 'ALJ', 'DOX', 'ACAS', 'AFG', 'ARII', 'ASI', 'CRMT', 'AMKR', 'NLY', 'ANH', 'ACGL', 'ARW', 'AIZ', 'ATW', 'AVT', 'AXLL', 'AXS', 'BLX', 'BKYF', 'BMRC', 'BKU', 'BANR', 'B', 'BBT', 'BBCN', 'BHLB', 'BOKF', 'CJES', 'CACI', 'CAP', 'COF', 'CMO', 'CFNL', 'CACB', 'CSH', 'CBZ', 'CNBC', 'CPF', 'CVX', 'CB', 'CNH', 'CMCO', 'CNOB', 'COP', 'CPSS', 'GLW', 'CROX', 'DO', 'DDS', 'DCOM', 'DYN', 'EWBC', 'EIHI', 'EBIX', 'EXXI', 'EFSC', 'EVER', 'RE', 'EZPW', 'FFG', 'FISI', 'FDEF', 'FIBK', 'NBCB', 'BANC', 'FRC', 'FRF', 'FCX', 'GM', 'GCO', 'GSOL', 'GS', 'GLRE', 'HBHC', 'HAFC', 'HDNG', 'HCC', 'HTLF', 'HELE', 'HEOP', 'HES', 'HMN', 'HUM', 'IM', 'IRDM', 'JOY', 'JPM', 'KALU', 'KCAP', 'KMPR', 'KSS', 'LBAI', 'LF', 'LINTA', 'LMCA', 'LCUT', 'LNC', 'LMIA', 'MTB', 'MGLN', 'MANT', 'MPC', 'MCGC', 'MDC', 'TAXI', 'MCC', 'MW', 'MOFG', 'MRH', 'MUR', 'MVC', 'MYRG', 'NOV', 'NCI', 'NAVG', 'NNI', 'NMFC', 'NNBR', 'NWPX', 'OLN', 'OVTI', 'OLP', 'PCCC', 'PRE', 'PMC', 'PSX', 'PHMD', 'PJC', 'PTP', 'PNC', 'BPOP', 'PFBC', 'PRI', 'PL', 'RF', 'RNR', 'REGI', 'RCII', 'RJET', 'RBCAA', 'SYBT', 'SAFT', 'SASR', 'SANM', 'SEM', 'SKH', 'SKYW', 'SFG', 'STT', 'STI', 'SPN', 'SYA', 'TAYC', 'TECD', 'TSYS', 'TICC', 'TWI', 'TITN', 'TOL', 'TMK', 'TWGP', 'TRV', 'TCBK', 'TRN', 'TRMK', 'TPC', 'UCBI', 'UNM', 'URS', 'USB', 'VLO', 'VR', 'VOXX', 'VSEC', 'WD', 'WRES', 'WBCO', 'WLP', 'WFC', 'WIBC', 'XRX', 'XL']

evenBetter = ['AWH', 'AFAM', 'ACAS', 'ASI', 'NLY', 'ANH', 'AIZ', 'AXS', 'BHLB', 'COF', 'CMO', 'DYN', 'FDEF', 'HMN', 'IM', 'IRDM', 'KMPR', 'LNC', 'LMIA', 'MANT', 'MCGC', 'MRH', 'MVC', 'NAVG', 'OVTI', 'PRE', 'PMC', 'PJC', 'PTP', 'BPOP', 'PL', 'RF', 'SKYW', 'STI', 'SPN', 'SYA', 'TECD', 'TSYS', 'TITN', 'TPC', 'UNM', 'VOXX', 'XL']


showCharts = raw_input('Would you like to show the financial data (Quandl) charts? (Y/N): ')

if showCharts.lower()=='y':
    print 'okay, charts will be shown'

elif showCharts.lwoer()=='n':
    print 'okay, charts will NOT be shown.'

else:
    print 'invalid input, charts will NOT be shown.'


def yahooKeyStats(stock):
    try:
        #print 'doing',stock
        sourceCode = urllib2.urlopen('http://finance.yahoo.com/q/ks?s='+stock).read()
        pbr = sourceCode.split('Price/Book (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        #print 'price to book ratio:',stock,pbr

        if float(pbr) < 1:
            #print 'price to book ratio:',stock,pbr

            PEG5 = sourceCode.split('PEG Ratio (5 yr expected)<font size="-1"><sup>1</sup></font>:</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
            if 0 < float(PEG5) < 2:
                #print 'PEG forward 5 years',PEG5

                DE = sourceCode.split('Total Debt/Equity (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
                #print 'Debt to Equity:',DE
                #if 0 < float(DE) < 2:
                PE12 = sourceCode.split('Trailing P/E (ttm, intraday):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
                #print 'Trailing PE (12mo):',PE12
                if float(PE12) < 15:

                    
                    print '______________________________________'
                    print ''
                    print stock,'meets requirements'
                    print 'price to book:',pbr
                    print 'PEG forward 5 years',PEG5
                    print 'Trailing PE (12mo):',PE12
                    print 'Debt to Equity:',DE
                    print '______________________________________'

                    if showCharts.lower() == 'y':

                        netIncomeAr = []
                        revAr = []
                        ROCAr = []

                        
                        endLink = 'sort_order=asc&auth_token=a3fpXxHfsiN7AF4gjakQ'
                        try:
                            netIncome = urllib2.urlopen('http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_'+stock+'_NET_INC.csv?&'+endLink).read()
                            revenue = urllib2.urlopen('http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_'+stock+'_REV_LAST.csv?&'+endLink).read()
                            ROC = urllib2.urlopen('http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_'+stock+'_ROC.csv?&'+endLink).read()

                            splitNI = netIncome.split('\n')
                            print 'Net Income:'
                            for eachNI in splitNI[1:-1]:
                                print eachNI
                                netIncomeAr.append(eachNI)

                            print '_________'
                            splitRev = revenue.split('\n')
                            print 'Revenue:'
                            for eachRev in splitRev[1:-1]:
                                print eachRev
                                revAr.append(eachRev)

                            
                            print '_________'
                            splitROC = ROC.split('\n')
                            print 'Return on Capital:'
                            for eachROC in splitROC[1:-1]:
                                print eachROC
                                ROCAr.append(eachROC)


                            incomeDate, income = np.loadtxt(netIncomeAr, delimiter=',',unpack=True,
                                                            converters={ 0: mdates.strpdate2num('%Y-%m-%d')})

                            revDate, revenue = np.loadtxt(revAr, delimiter=',',unpack=True,
                                                            converters={ 0: mdates.strpdate2num('%Y-%m-%d')})

                            rocDate, ROC = np.loadtxt(ROCAr, delimiter=',',unpack=True,
                                                            converters={ 0: mdates.strpdate2num('%Y-%m-%d')})

                            fig = plt.figure()
                            
                            ax1 = plt.subplot2grid((6,6),(0,0), rowspan=2, colspan=6)
                            ax1.plot(incomeDate, income)
                            plt.ylabel('Net Income (m)')

                            ax2 = plt.subplot2grid((6,6),(2,0), sharex=ax1, rowspan=2, colspan=6)
                            ax2.plot(revDate, revenue)
                            plt.ylabel('Revenue')

                            ax3 = plt.subplot2grid((6,6),(4,0), sharex=ax1, rowspan=2, colspan=6)
                            ax3.plot(rocDate, ROC)
                            plt.ylabel('ROC')

                            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                            plt.subplots_adjust(hspace=0.53)

                            plt.suptitle(stock) 

                            
                            plt.show()

                        except Exception, e:
                            print 'failed the main quandl loop for reason of',str(e)
  
    except Exception,e:
        #print 'failed in the main loop',str(e)
        pass


for eachStock in ofInterest:
    yahooKeyStats(eachStock)
    #time.sleep(.2)

print evenBetter