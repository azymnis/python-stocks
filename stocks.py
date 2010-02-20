import urllib2
import logging
import sys
import csv
import time
import datetime
from pylab import *
from operator import itemgetter

#Logging stuff....
logger = logging.getLogger("STOCKS")
logger.setLevel(logging.DEBUG)
shandle = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
shandle.setFormatter(formatter)
logger.addHandler(shandle)

MIN_ZVALUE = 1.5
MIN_LOOKBACK = 5
STOCK_FILES = ["sp500.csv","nasdaq100.csv"]
#STOCK_FILES = ["nasdaq100.csv"]

class Stock(object):
    """
    This class holds historical stock information.
    """

    YF_URL = "http://ichart.finance.yahoo.com/table.csv?s="
    DATE_STRING = "Date"
    CLOSE_STRING = "Close"
    MAX_YEARS_LOOKBACK = 10

    def __createDateMap(self,page):
        """
        Reads the csv file from yahoo finance and creates a date map
        containing historical stock info.
        """
        inReader = csv.reader(page)
        
        #Reader header and get Date and Close index
        header = inReader.next()
        try:
            dateInd = header.index(Stock.DATE_STRING)
            closeInd = header.index(Stock.CLOSE_STRING)
        except ValueError:
            logger.warn("could not find date or close index in csv header")
        
        #put closing dates on map
        self.close = {}
        for line in inReader:
            date = getDateFromString(line[dateInd])
            closeValue = float(line[closeInd])
            self.close[date] = closeValue
        
    def __init__(self,tickerSymbol):
        """
        Constructor takes as argument stock ticker symbol.
        """
        self.name = tickerSymbol
        dataUrl = Stock.YF_URL+tickerSymbol
        page = urllib2.urlopen(dataUrl)
        try:
            logger.debug("reading data for stock %s" % tickerSymbol)
            self.__createDateMap(page)
        except Exception:
            logger.warn("could not read data")
        page.close()

    def getClosingPriceForRange(self,start,end):
        """
        Returns a list of the stock close price for the date range specified.
        The dates should be strings with format YYYY-MM-DD
        """
        stocksInRange = [s for s in self.close.items()
                            if s[0] >= start
                            and s[0] <= end]
        stocksInRange = sorted(stocksInRange,key=itemgetter(0))
        return [s[1] for s in stocksInRange]
    
    def containsDate(self,date):
        """
        Checks if dict with closing prices contains a given date.
        """
        return date >= min(self.close.keys())

    def getMaxReturnForPeriod(self,start,end):
        """
        Goes through closing prices for period and returns the maximum possible return
        for this time period.
        """
        prices = self.getClosingPriceForRange(start,end)
        stockReturns = [(p-prices[0])/prices[0] for p in prices[1:]]
        return max(stockReturns)

    def getHistoricalMaxReturn(self,start,end):
        """
        Returns a list of max returns over the years for this period.
        E.g. if start = 2010-01-01 and end = 2010-02-30,
        this checks for returns for periods:
        (2009-01-01,2009-02-30),(2008-01-01,2008,02-30),...
        Always assumes that period is less than a year.
        """
        delta = datetime.timedelta(days=-365)
        stockReturns = []
        for i in range(Stock.MAX_YEARS_LOOKBACK):
            start = start+delta
            end = end+delta
            if not self.containsDate(start):
                break
            stockReturns.append(self.getMaxReturnForPeriod(start,end))
        return stockReturns

def getDateFromString(dateString):
    """
    Converts a string into a datetime.date object.
    """
    curTime = time.strptime(dateString,"%Y-%m-%d")
    return datetime.date(curTime.tm_year,curTime.tm_mon,curTime.tm_mday)

def readStocksFromFile():
    """
    Returns a list of stock ticker symbols read from selected files.
    """
    stocks = set([])
    for file in STOCK_FILES:
        logger.debug("reading ticker names from file: %s" % file)
        reader = csv.reader(open(file))
        stocks |= set([line[0] for line in reader])
    return stocks 

def writeResultsToFile(returnMap,start,end,fileName):
    """
    Writes returnMap to specified file.
    """
    logger.debug("writing results to file")
    writer = csv.writer(open(fileName,"w"))
    sortedReturns = sorted(returnMap.items(),key=itemgetter(1),reverse=True)
    writer.writerow(["start: %s " % start,"end: %s" % end])
    writer.writerow(["symbol","mean","std-deviation","z-value","lookback years"])
    for v in sortedReturns:
        writer.writerow([v[0],v[1][1],v[1][2],v[1][0],v[1][3]])

def getStockReturns(stockNames):
    """
    Given a list of stock names gets their returns and puts them in a map
    that contains
    name -> z-value,mean,std,lookbackYears
    """
    stockReturns = {}
    for name in stockNames:
        try:
            curStock = Stock(name)
            curReturns = curStock.getHistoricalMaxReturn(start,end)
            curMean = mean(curReturns)
            curStd = std(curReturns)
            curZ = curMean/curStd
            yearsBack = len(curReturns)
            stockReturns[name] = (curZ,curMean,curStd,yearsBack)
            if curZ >= MIN_ZVALUE and yearsBack >= MIN_LOOKBACK:
                logger.debug("stock returns %s" % curReturns)
                logger.debug("z-value: %s, mean: %s, std: %s, years: %s" % tuple(stockReturns[name]))
        except Exception, e:
            logger.warn("skipping stock %s because of error: '%s'" % (name,e))
    return stockReturns

def plotResults(stockReturns):
    """
    Plots the returns that satisfy some criteria...
    """
    #Plot results
    for name in stockReturns:
        res = stockReturns[name]
        if res[0] >= MIN_ZVALUE and res[3] >= MIN_LOOKBACK:
            plot([res[1]],[res[2]],'bo')
            text(res[1]+0.0001,res[2]+0.0001,name)
    show()

if __name__=='__main__':
    if len(sys.argv)<3:
        print """
        Usage: python stocks.py <start date> <end date>
        
        Date Format: YYYY-MM-DD
        """
        sys.exit(1)
    #get start and end
    start = getDateFromString(sys.argv[1])
    end = getDateFromString(sys.argv[2])
    
    #now do all the computation
    stockNames = readStocksFromFile()
    stockReturns = getStockReturns(stockNames)
    writeResultsToFile(stockReturns,start,end,"stockResults.csv")
    plotResults(stockReturns)
