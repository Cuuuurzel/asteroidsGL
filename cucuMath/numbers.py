import math
      
    
class Complex() :

    def __init__( self, r, i=0 ) :
        self.r = r
        self.i = i

    def reciprocal( self ) :
        return self.conjugate() / abs( self )

    def conjugate( self ) :
        return Complex( self.r, -self.i )
    
    def __abs__( self ) :
        return math.sqrt( self.r**2 + self.i**2 )
    
    def __add__( self, n ) :
        try : 
            return Complex( self.r+n.r, self.i+n.i )
        except AttributeError :
            return Complex( self.r+n, self.i )
        
    def __div__( self, n ) :
        try :
            return self * n.reciprocal()
        except AttributeError :
            return Complex( self.r/n, self.i )

    def __mul__( self, n ) :
        try :
            return Complex( self.r*n.r - self.i*n.i, self.i*n.r + self.r*n.i )
        except AttributeError :
            return Complex( self.r*n, self.i )

    def __neg__( self ) : 
        return Complex( -self.r, -self.i )

    def __pow__( self, n ) :
        x = 1
        for e in range( 0, n+1 ) : x *= self
        return x 

    def __sub__( self, n ) :
        return self + n.__neg__()

    def __str__( self ) :
        s = str( self.r )
        if self.i != 0 :
            if self.i > 0 :
                return s + " + " + str( self.i ) + "i"
            else : return s + " " + str( self.i ) + "i"
        else : return s
            
