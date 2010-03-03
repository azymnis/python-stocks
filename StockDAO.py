import datetime
import time
import csv
import Stock

#Logging stuff....
logger = logging.getLogger("STOCKS")
logger.setLevel(logging.DEBUG)
shandle = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
shandle.setFormatter(formatter)
logger.addHandler(shandle)


SP = "S&P"
NSDQ = "NSDQ"
NYSE = "NYSE"

STOCK_FILE = { SP:"sp500.csv", NSDQ: "nasdaq100.csv", NYSE:"nyse.csv" }


class StockDAO( object ):
    data = {}
    PRICE = CLOSE
    def __init__( self, stocks = None, index = None, price = PRICE ):
        PRICE = price
        tickers = []
        if( not stocks == None ):
            tickers = stocks
        elif( not index == None ):
            tickers = Stock.readStocksFromFile( files = STOCK_FILE[ index ] )
        
        for ticker in tickers:
            self.data[ ticker ] = Stock( ticker, price = price )
    def getPrice( self,ticker, date ):
        if( not data.has_key( ticker ) ):
            self.data[ ticker ] = Stock( ticker, price = price );
            self.data[ ticker ].initData()
        else:
            return data[ ticker ].getPrice( date )
            
    def getPreviousPrice( self, ticker, date ):
        if( not data.has_key( ticker ) ):
            self.data[ ticker ] = Stock( ticker, price = price );
            self.data[ ticker ].initData()
        self.data[ ticker ].getPreviousPrice( ticker, date )      
                                    
        
