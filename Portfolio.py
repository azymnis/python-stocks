import Stock.py

class Portfolio( Object ):
    stocks = {}
    value = {}
    pnl = {}
    shortCash = 0.0
    longCash = 0.0
    defIR = 0.04
    def __init__(IR = defIR):
        this.IR = IR

    def buy( self, ticker, price, shares):
        if( stocks.has_key( ticker  ) and stocks[ ticker ] < 0 ):
            raise Exception( "can't buy when you're short shares already " )
        shortCash-= price * shares;
        stocks[ ticker ] = stocks[ ticker ].get( ticker, 0 ) + shares

    def sellShort( self, ticker, price, shares ):
        longCash += price * shares
        if( stocks.has_key( ticker ) ):
            if( stocks[ticker] > 0):
                raise Exception( "can't sell short when you're long the stock " + ticker ):
            else:
                stocks[ ticker ] -= shares
        else:
            stocks[ ticker ] -= shares

    def sell( self, ticker, price, shares ):
        if( stocks.has_key( ticker ) and ( stocks[ ticker ] < 0 or stocks[ ticker ] < shares )):
            raise Exception( "can't sell when you're short or have more than " + stocks[ ticker ] + " shares " )

        shortCash+= price * shares;
        stocks[ ticker ] = stocks.get( ticker, 0 ) + shares
                
    def buyToCover( self, ticker, price, shares ):
        if( stocks.has_key( ticker ) and ( stocks[ ticker ] > 0 or abs( stocks[ ticker ] ) < shares )):
            raise Exception( "can't buyToCover when you're long or are short less than " + stocks[ ticker ] + " shares " )

        longCash-= price * shares;
        stocks[ ticker ] = stocks.get( ticker, 0 ) + shares

    def doCarry(self):
        longCash*=pow( 1 + this.IR, 1/365 )

    def mark( self, iter ):
        for stock, shares in stocks.items():
            oldValue = value[ max( value.keys() ) ]
            value[ iter.currDate() ] = (iter.getPrice( stock.getTicker() ) - stock.getLastPrice()) * shares;
            pnl[ iter.currDate() ] = value[ iter.currDate() ] - oldValue
    
    def isLong( self, ticker ):
        if( stocks.has_key( ticker ) && stocks[ ticker ] > 0 ):
            return True
        else:
            return False
 
    def isShort( self, ticker ):
        if( stocks.has_key( ticker ) && stocks[ ticker ] < 0 ):
            return True
        else:
            return False


    def isFlat( self, ticker ):
        if( not stocks.has_key( ticker ) or stocks[ ticker ] == 0 ):
            return True
        else:
            return False 
