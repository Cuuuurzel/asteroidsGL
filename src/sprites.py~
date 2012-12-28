from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from src.geometry import *
from src.moregl import *

class GLSprite2d() :

    def __init__( self, isCircle, rect, currentMotion, box ) :
        self.currentMotion = currentMotion
        self.rect = rect
        self.box = box
        self.z = 0
        self.toKeepInBox = not box is None
        self.color = ( 0, 255, 0, 1 )
        self.isCircle = isCircle
        self.circle = Circle( self.rect.center(), self.rect.w/2 )

    def update( self ) :
        self.rect.moveOf( self.currentMotion[0], self.currentMotion[1] )
        if self.toKeepInBox : self.keepInBox()

    def blit( self ) :
        glMaterialfv( GL_FRONT, GL_DIFFUSE, self.color )
        if not self.isCircle :
            glBegin( GL_QUADS )
            glVertex( self.rect.x, self.rect.y, self.z )
            glVertex( self.rect.x+self.rect.w, self.rect.y, self.z )
            glVertex( self.rect.x+self.rect.w, self.rect.y+self.rect.h, self.z )
            glVertex( self.rect.x, self.rect.y+self.rect.h, self.z )
            glEnd()
        else :
            glCircle( self.circle.c, self.circle.r )
            
    def collide( self, sprite ) :
        if sprite.isCircle and self.isCircle :            
            return self.circle.collideCircle( sprite.circle )
        elif sprite.isCircle and not self.isCircle :
            return sprite.circle.collideRect( self.rect )
        elif not sprite.isCircle and self.isCircle :
            return self.rect.collideRect( sprite.rect )
        else :
            return self.rect.collideRect( sprite.rect )
        
    def keepInBox( self ) :
        if not self.isInBox() :
            nx = self.rect.x
            ny = self.rect.y
            if self.rect.x > self.box.w-self.rect.w/2 :
                nx = self.box.x - self.rect.w/2
            if self.rect.x < self.box.x :
                nx = self.box.x+self.box.w - self.rect.w/2
            if self.rect.y > self.box.h-self.rect.h/2 :
                ny = self.box.y - self.rect.h/2
            if self.rect.y < self.box.y :
                ny = self.box.y+self.box.h - self.rect.h/2
            self.rect.moveTo( nx, ny )
            self.circle.moveTo( nx, ny )
            
    def isInBox( self ) :
        isin = False
        if self.isCircle and self.circle.collideRect( self.box ) :
            isin = True
        if not self.isCircle and self.rect.collideRect( self.box ) :
            isin = True
        return isin


class GLSprite3d() :

    def __init__( self, body, currentMotion, box ) :
        self.currentMotion = currentMotion
        self.body = body
        self.box = box
        self.toKeepInBox = not box is None
        self.color = ( 0, 1, 0, 1 )
        self.isSphere = body.__class__ == Sphere
        self.isCube = False #usa glutSolidCube per disegnare

    def update( self ) :
        self.body.moveOf( self.currentMotion[0], self.currentMotion[1], self.currentMotion[2] )
        if self.toKeepInBox : self.keepInBox()

    def blit( self ) :
        glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, self.color )
        glPushMatrix()
        if self.isCube :
            glTranslate( self.body.pos[0]-self.body.w/2, 
                         self.body.pos[1]-self.body.w/2, 
                         self.body.pos[2]-self.body.w/2 )
            glutSolidCube( self.body.w )        
        elif not self.isSphere :
            glTranslate( self.body.pos[0]-self.body.w/2, 
                         self.body.pos[1]-self.body.h/2, 
                         self.body.pos[2]-self.body.l/2 )
            glParallelepiped( self.body.w, self.body.h, self.body.l )
        else :
            glTranslate( self.body.pos[0], self.body.pos[1], self.body.pos[2] )
            glutSolidSphere( self.body.r, self.body.quality[0], self.body.quality[1] )
        glPopMatrix()
    
    def collide( self, sprite ) :
        if sprite.isSphere and self.isSphere :            
            return self.body.collideSphere( sprite.body )
        elif sprite.isSphere and not self.isSphere :
            return sprite.body.collideParallelepiped( self.body )
        elif not sprite.isSphere and self.isSphere :
            return self.body.collideParallelepiped( sprite.body )
        else :
            return self.body.collideParallelepiped( sprite.body )
    
    def keepInBox( self ) :
        if not self.isInBox() :
            nx = self.body.pos[0]
            ny = self.body.pos[1]
            nz = self.body.pos[2]
            if self.body.pos[0] > self.box.pos[0]+self.box.w :
                nx = self.box.pos[0]              
            elif self.body.pos[0] < self.box.pos[0] :
                nx = self.box.pos[0]+self.box.w  
            if self.body.pos[1] > self.box.pos[1]+self.box.h :
                ny = self.box.pos[1]              
            elif self.body.pos[1] < self.box.pos[1] :
                ny = self.box.pos[1]+self.box.h       
            if self.body.pos[2] > self.box.pos[2]+self.box.l :
                nz = self.box.pos[2]                
            elif self.body.pos[2] < self.box.pos[2] :
                nz = self.box.pos[2]+self.box.l       
            if self.isSphere :
                r2 = self.body.r/2
                self.body.moveTo( nx+r2, ny+r2, nz+r2 )
            else :
                self.body.moveTo( nx, ny, nz )

    def isInBox( self ) :
        return self.body.collideParallelepiped( self.box )
