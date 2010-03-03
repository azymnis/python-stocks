import StockIterator
import Stock
import Portfolio

class TitTatStrategy( Object ):
    
    def __init__(self, ticker):
        self.ticker = ticker

    def initParams( str ):
        self.ticker = str

    def run( iter, portf ):
        currPrice = iter.getPrice( self.ticker )
        lastPrice = iter.getPreviousPrice( self.ticker )
        if( currPrice > lastPrice ):
            if( portf.isShort( self.ticker )  or portf.isFlat( self.ticker ) ):
                portf.sellShort( self.ticker, currPrice, 1 )
            elif( portf.isLong( self.ticker ) ):
                portf.sell( self.ticker, currPrice, 1 )
                
        elif( currPrice < lastPrice ):
            if( portf.isLong( self.ticker ) or portf.isFlat( self.ticker )):
                portf.buy( self.ticker, currPrice, 1 )
            elif( portf.isShort( self.ticker ) ):
                portf.buyToCover( self.ticker, currPrice, 1 )
        
        
