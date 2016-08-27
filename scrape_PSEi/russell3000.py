import time
import urllib2
from urllib2 import urlopen

#download list from russell 3000 pdf website and save as rrussell300.txt

tickers = []		

def parseRus():
    try:
        readFile = open('russell3000.txt','r').read()
        splitFile = readFile.split('\n')
        for eachLine in splitFile:
            splitLine = eachLine.split(' ')
            ticker = splitLine[-1]
            tickers.append(ticker)

        print tickers
                

    except Exception,e:
        print 'failed in the main loop',str(e)


parseRus()