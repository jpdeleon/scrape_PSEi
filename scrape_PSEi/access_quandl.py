#cd ../../Google Drive/project/B_finance/fund_invest
#try quandl to download pse dataimport time
import urllib2
from urllib2 import urlopen


def grabQuandl(ticker):
    endLink = 'sort_order=asc'

    try:
        #Keep in mind this will result in 3 requests# ... so dont run the heck out of this.
        netIncome = urllib2.urlopen('http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_'+ticker+'_NET_INC.csv?&'+endLink).read()
        revenue = urllib2.urlopen('http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_'+ticker+'_REV_LAST.csv?&'+endLink).read()
        ROC = urllib2.urlopen('http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_'+ticker+'_ROC.csv?&'+endLink).read()
https://www.quandl.com/data/YAHOO/AAPL
        print netIncome
        print '__________________'
        print revenue
        print '__________________'
        print ROC
        print '__________________'
        
    except Exception,e:
        print 'failed in the main loop due to:',str(e)
        pass

grabQuandl('YHOO')