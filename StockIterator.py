import StockDAO
import Stock

class StockIterator( Object ):
    def __init__( self, index, startDate, endDate, price = Stock.CLOSE ):
        this.dao = StockDAO( index = index, price = price )
        this.currDate = startDate
    def nextDay(self):
        if( startDate > endDate ):
            return False
        else:
            this.currDate += datetime.timedelta(days=1 )
            return True
    def getDAO(self):
        return self.dao
    
    def getPrice( self,ticker ):
        self.dao.getPrice( ticker, currDate ) 
    
    def getPreviousPrice( self, ticker ):
        self.dao.getPreviousPrice( ticker, currDate )
              
