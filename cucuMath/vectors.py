import math

X = 0
Y = 1
Z = 2

class GenericVector( list ) :
    
    def __init__( self, elements ) :
        list.__init__( self, elements )

    def lenght( self ) :
        return len( self )

    def reduce( self ) :
        if not self.isNull() :
            m = self.module()
            for i, v in enumerate( self ) : self[i] = v/m
        
    def module( self ) :
        summ = 0
        for i in self : summ += i**2
        return math.sqrt( summ )

    def isNull( self ) :
        if self.module() == 0 : return True
        else: return False

    def __add__( self, v ) :
        l = []
        for i, e in enumerate( self ) : l.append( e + v[i] )
        return GenericVector( l )

    def __mul__( self, k ) :
        l = []
        for e in self : l.append( e*k )
        return GenericVector( l )

    def __iadd__( self, v ) :
        return self.__add__( v )

    def __imul__( self, k ) :
        return self.__mul__( k )
    
        
class Vector2d( GenericVector ) :

    def __init__( self, x, y=None ) :
        if y is None :
            GenericVector.__init__( self, x )
        else : GenericVector.__init__( self, [ x, y ] )
        self.currentAngle = self._calcAngle()

    def _calcAngle( self ) :
        if not self.isNull() :
            return math.atan2( self[Y], self[X] )            
        else : return 0

    def angleWith( self, otherVector ) :
        if len( otherVector ) < 2 :
            raise TypeError( "The given vector must have at least 2 elements!" )
        if len( otherVector ) > 2 :
            try :
                return otherVector.angleWith( self )
            except :
                return Vector3d( otherVector ).angleWith( self )
        return abs( self.currentAngle - otherVector.currentAngle )          
    
    def phase( self ) :
        return math.atan2( self[Y], self[X] )

    def rotate( self, angle ) :
        self.currentAngle += angle
        m = self.module()
        self[0] = math.cos( self.currentAngle ) * m
        self[1] = math.sin( self.currentAngle ) * m 

    def setAngle( self, angle ) :
        self.currentAngle = angle
        m = self.module()
        self[0] = math.cos( self.currentAngle ) * m
        self[1] = math.sin( self.currentAngle ) * m 

    def __add__( self, v ) :
        return Vector2d( GenericVector.__add__( self, v ) )

    def __mul__( self, k ) :
        return Vector2d( GenericVector.__mul__( self, k ) )
