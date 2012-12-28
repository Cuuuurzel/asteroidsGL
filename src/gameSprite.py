import random

from src.exceptions import *
from src.gameConst import *
from src.sprites import *
from cucuMath.vectors import *

class Ship( GLSprite3d ) :

    def __init__( self, pos ) :
        body = Sphere( pos, SHIP_SIZE )
        body.quality = [ int( body.r * SPHERE_FINEST_COEFF * 3 ), 
                         int( body.r * SPHERE_FINEST_COEFF * 3 ) ]
        GLSprite3d.__init__( self, body, (0,0,0), SCREEN )
        self.color = SHIP_COLOR
        self.usedBullets = []
        self.gaze = Vector2d( 1, 0 )
        self.lastMousePos = pos
        self.shootCount = 0

    def shoot( self ) :
        if self.shootCount > 0 :
            self.shootCount -= 1
            newShoot = Bullet( self.body.pos, self.gaze )
            self.usedBullets.append( newShoot )

    def blit( self ) :
        GLSprite3d.blit( self )
        for b in self.usedBullets :
            b.blit()

    def update( self ) :
        GLSprite3d.update( self )
        for b in self.usedBullets :
            b.update()
        self._rotate()
    
    def _rotate( self ) :
        ax = self.body.pos[0] + SCREEN.w/2
        ay = self.body.pos[1] + SCREEN.h/2
        mx = self.lastMousePos[0] - ax
        my = self.lastMousePos[1] - ay
        self.gaze = Vector2d( mx, -my )
        self.gaze.reduce()

    def _updateMotion2d( self, v ) :
        vm = Vector2d( self.currentMotion[0], self.currentMotion[1] )
        vr = vm + v
        if vr.module() > MAX_SHIP_SPEED :
            vr.reduce()
            vr *= MAX_SHIP_SPEED
        self.currentMotion = vr[0], vr[1], 0

    def turnLeft( self ) : 
        self._updateMotion2d( [ -KEYS_WEIGHT, 0 ] )

    def turnRight( self ) : 
        self._updateMotion2d( [ KEYS_WEIGHT, 0 ] )

    def turnDown( self ) : 
        self._updateMotion2d( [ 0, -KEYS_WEIGHT ] )

    def turnUp( self ) : 
        self._updateMotion2d( [ 0, KEYS_WEIGHT ] )


class Bullet( GLSprite3d ) :
    
    def __init__( self, shipPos, d ) :
        body = Sphere( shipPos, BULLET_SIZE )
        v = Vector2d( d[0], d[1] )
        v.reduce()
        v *= BULLET_SPEED
        v = v[0], v[1], 0
        GLSprite3d.__init__( self, body, v, SCREEN )
        self.color = BULLET_COLOR
        self.tokeepInBox = False
        self.isDead = False
        self.toKeepInBox = False

    def blit( self ) :       
        glBegin( GL_POINTS )
        glVertex( self.body.pos[0], self.body.pos[1], self.body.pos[2] )
        glEnd()


class Asteroid( GLSprite3d ) :

    def __init__( self, l, p=None, d=None ) :
        self.lv = l
        r = int( l * ASTEROID_SIZE )
        if p is None : p = self.randomPosition( r/2 )
        if d is None : d = self.randomDirection()
        body = Sphere( p, r )
        body.quality = [ int( body.r * SPHERE_FINEST_COEFF ), 
                         int( body.r * SPHERE_FINEST_COEFF ) ]
        GLSprite3d.__init__( self, body, d, SCREEN )
        self.color = ASTEROID_COLOR
        self.isDead = False
        
    def randomPosition( self, r ) :
        x = random.randint( SCREEN.pos[0]-2*r, SCREEN.pos[0]+SCREEN.w+2*r )
        if x < -r or x > SCREEN_SIZE[0] :
            y = random.randint( SCREEN.pos[1]-2*r, SCREEN.pos[1]+SCREEN.h+2*r )
        else :
            y1 = SCREEN.pos[1] - random.randint( r, 2*r )
            y2 = SCREEN.pos[1] + SCREEN.h + random.randint( r, 2*r )
            y = random.choice( [ y1, y2 ] )
        return [ x, y, GAME_Z ]

    def randomDirection( self ) :
        v = Vector2d( random.randint( -DIR_RATIO, DIR_RATIO ),\
                      random.randint( -DIR_RATIO, DIR_RATIO ) )
        v.reduce()
        v *= ASTEROIDS_SPEED    
        return [ v[0], v[1], 0 ]

    def split( self ) :
        if self.lv < 2 : return []
        else :
            newa = []
            newlevel = self.lv * LEVEL_DEC
            dang = AST_DIR_ANG/SPLIT_N
            ang = -math.pi/2
            for i in range( 0, SPLIT_N ) :
                nv = Vector2d( self.currentMotion[0], self.currentMotion[1] )
                nv.rotate( ang )
                ang += dang
                na = Asteroid( newlevel, self.body.pos, [ nv[0], nv[1], GAME_Z ] )
                newa.append( na )
            for i in range( 0, INCUBATION ) :
                for a in newa :
                    a.update()
            return newa
    
    def collide( self, sprite ) :
        if sprite.__class__ == Bullet :
            return self.body.collidePoint( sprite.body.pos )
        else :
            return GLSprite3d.collide( self, sprite ) 
