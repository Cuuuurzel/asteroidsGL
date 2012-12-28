import math

class Rect() :

    def __init__( self, x, y, w=None, h=None ) :
        if w is None :
            self.w = y[0]
            self.h = y[1]
            self.y = x[1]
            self.x = x[0]
        else :
            self.x = x
            self.w = w
            self.h = h
            self.y = y

    def moveTo( self, x, y ) :
        self.x = x
        self.y = y

    def moveOf( self, dx, dy ) :
        self.moveTo( self.x+dx, self.y+dy )

    def topLeft( self ) :
        return [ self.x, self.y ]

    def center( self ) :
        return [ self.x+self.w/2, self.y+self.h/2 ]

    def bottomRight( self ) :
        return [ self.x+self.w, self.y+self.h ]

    def topRight( self ) :
        return [ self.x+self.w, self.y ]

    def bottomLeft( self ) :
        return [ self.x, self.y+self.h ]

    def collidePoint( self, px, py=None ) :
        if py is None : point = px
        else : point = px, py
        coll = False
        if self.x <= point[0] <= self.x+self.w :
            if self.y <= point[1] <= self.y+self.h :
                coll = True
        return coll            

    def collideRect( self, rect ) :
        coll = False
        if ( self.collidePoint( rect.x,        rect.y ) or
             self.collidePoint( rect.x,        rect.y+rect.w ) or
             self.collidePoint( rect.x+rect.h, rect.y+rect.w ) or
             self.collidePoint( rect.x+rect.h, rect.y ) or

             rect.collidePoint( self.x,        self.y ) or
             rect.collidePoint( self.x,        self.y+self.w ) or
             rect.collidePoint( self.x+self.h, self.y+self.w ) or
             rect.collidePoint( self.x+self.h, self.y ) ) :
            coll = True
        return coll


class Parallelepiped() :

    def __init__( self, pos, w, h, l ) :
        self.pos = pos
        self.w = w
        self.l = l
        self.h = h

    def moveTo( self, x, y, z ) :
        self.pos = [ x, y, z ]

    def moveOf( self, dx, dy, dz) :
        self.moveTo( self.pos[0]+dx, self.pos[1]+dy, self.pos[2]+dz )

    def center( self ) :
        return [ self.pos[0]+self.w/2,
                 self.pos[1]+self.h/2,
                 self.pos[2]+self.l/2 ]

    def collidePoint( self, px, py=None, pz=None ) :
        if py is None and pz is None :
            point = px
        elif pz is None :
            point = px, py, 0
        else : point = px, py, pz
        coll = False
        if self.pos[0] <= point[0] <= self.pos[0]+self.w :
            if self.pos[1] <= point[1] <= self.pos[1]+self.h :
                if self.pos[2] <= point[2] <= self.pos[2]+self.l :
                    coll = True
        return coll            

    def collideParallelepiped( self, p ) :
        coll = False
        if ( self.collidePoint( p.pos[0],     p.pos[1],     p.pos[2] ) or
             self.collidePoint( p.pos[0]+p.w, p.pos[1],     p.pos[2] ) or
             self.collidePoint( p.pos[0]+p.w, p.pos[1]+p.h, p.pos[2] ) or
             self.collidePoint( p.pos[0],     p.pos[1]+p.h, p.pos[2] ) or
             
             self.collidePoint( p.pos[0],     p.pos[1],     p.pos[2]+p.l ) or
             self.collidePoint( p.pos[0]+p.w, p.pos[1],     p.pos[2]+p.l ) or
             self.collidePoint( p.pos[0]+p.w, p.pos[1]+p.h, p.pos[2]+p.l ) or
             self.collidePoint( p.pos[0],     p.pos[1]+p.h, p.pos[2]+p.l ) or
             
             p.collidePoint( self.pos[0],        self.pos[1],        self.pos[2] ) or
             p.collidePoint( self.pos[0]+self.w, self.pos[1],        self.pos[2] ) or
             p.collidePoint( self.pos[0]+self.w, self.pos[1]+self.h, self.pos[2] ) or
             p.collidePoint( self.pos[0],        self.pos[1]+self.h, self.pos[2] ) or
             
             p.collidePoint( self.pos[0],        self.pos[1],        self.pos[2]+self.l ) or
             p.collidePoint( self.pos[0]+self.w, self.pos[1],        self.pos[2]+self.l ) or
             p.collidePoint( self.pos[0]+self.w, self.pos[1]+self.h, self.pos[2]+p.l ) or
             p.collidePoint( self.pos[0],        self.pos[1]+self.h, self.pos[2]+self.l ) ) :
            coll = True
        return coll


class Circle() :

    def __init__( self, cx, cy, r=None ) :
        if r is None :
            self.c = cx
            self.r = cy
        else :
            self.c = [ cx, cy ]
            self.r = r

    def moveTo( self, x, y ) :
        self.c = [ x, y ]

    def moveOf( self, dx, dy ) :
        self.moveTo( self.c[0]+dx, self.c[1]+dy )

    def collidePoint( self, px, py=None ) :
        if py is None : point = px
        else : point = px, py
        coll = False
        x = point[0] - self.c[0]
        y = point[1] - self.c[1]
        if math.sqrt( x**2 + y**2 ) < self.r : coll = True
        return coll

    def collideCircle( self, circle ) :
        coll = False
        x = circle.c[0] - self.c[0]
        y = circle.c[1] - self.c[1]
        if math.sqrt( x**2 + y**2 ) < circle.r+self.r : coll = True
        return coll

    def collideRect( self, rect ) :
        coll = False
        closestPoint = [ self.c[0], self.c[1] ]
        if self.c[0] < rect.x :
            closestPoint[0] = rect.x
        elif self.c[0] > rect.x+rect.w :
            closestPoint[0] = rect.x+rect.w
        if self.c[1] < rect.y :
            closestPoint[1] = rect.y
        elif self.c[1] > rect.y+rect.h :
            closestPoint[1] = rect.y+rect.h            
        diff = closestPoint[0]-self.c[0], closestPoint[1]-self.c[1]
        if not diff[0]*diff[0] + diff[1]*diff[1] > self.r**2 : coll = True
        return coll


class Sphere() :

    def __init__( self, c, r ) :
        self.pos = c
        self.quality = 15, 15
        self.r = r

    def moveTo( self, x, y, z ) :
        self.pos = [ x, y, z ]

    def moveOf( self, dx, dy, dz) :
        self.moveTo( self.pos[0]+dx, self.pos[1]+dy, self.pos[2]+dz )

    def collidePoint( self, px, py=None, pz=None ) :
        if py is None : point = px
        elif pz is None : point = px, py, 0
        else : point = px, py, pz
        coll = False
        x = point[0] - self.pos[0]
        y = point[1] - self.pos[1]
        z = point[2] - self.pos[2]
        if x**2 + y**2 + z**2 < self.r : coll = True
        return coll

    def collideSphere( self, sphere ) :
        coll = False
        x = sphere.pos[0] - self.pos[0]
        y = sphere.pos[1] - self.pos[1]
        z = sphere.pos[2] - self.pos[2]
        if math.sqrt( x**2 + y**2 + z**2 ) < sphere.r+self.r : coll = True
        return coll

    def collideParallelepiped( self, par ) :
        coll = False 
        c1 = par.pos
        c2 = par.pos[0]+par.w, par.pos[1]+par.h, par.pos[2]+par.l
        d_squared = self.r**2
        if ( self.pos[0] < c1[0] ) :   d_squared -= ( self.pos[0] - c1[0] )**2
        elif ( self.pos[0] > c2[0] ) : d_squared -= ( self.pos[0] - c2[0] )**2
        if ( self.pos[1] < c1[1] ) :   d_squared -= ( self.pos[1] - c1[1] )**2
        elif ( self.pos[1] > c2[1] ) : d_squared -= ( self.pos[1] - c2[1] )**2
        if ( self.pos[2] < c1[2] ) :   d_squared -= ( self.pos[2] - c1[2] )**2
        elif ( self.pos[2] > c2[2] ) : d_squared -= ( self.pos[2] - c2[2] )**2
        if d_squared > 0 or par.collidePoint( self.pos ) : coll = True
        return coll
