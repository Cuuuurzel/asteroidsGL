from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math

def glCircle( center, r, i=None ) :
    if i is None: i = r * 100
    a = 0
    x = 2*math.pi/i
    glBegin( GL_LINES )
    while a < math.pi*2 :
        glVertex( center[0], center[1] )
        glVertex( r*math.cos(a), r*math.sin(a) )
        a += x
    glEnd()

def glParallelepiped( w, h, l ) :
    glBegin( GL_TRIANGLE_STRIP )
    glVertex( 0, 0, 0 )
    glVertex( w, 0, 0 )
    glVertex( w, h, 0 )
    glVertex( 0, h, 0 )
    glVertex( 0, 0, 0 )
    glEnd()
    glBegin( GL_TRIANGLE_STRIP )
    glVertex( 0, 0, l )
    glVertex( w, 0, l )
    glVertex( w, h, l )
    glVertex( 0, h, l )
    glVertex( 0, 0, l )
    glEnd()
    glBegin( GL_TRIANGLE_STRIP )
    glVertex( 0, 0, 0 )
    glVertex( 0, 0, l )
    glVertex( 0, h, l )
    glVertex( 0, 0, 0 )
    glVertex( 0, h, 0 )
    glEnd()
    glBegin( GL_TRIANGLE_STRIP )
    glVertex( w, 0, 0 )
    glVertex( w, 0, l )
    glVertex( w, h, l )
    glVertex( w, h, 0 )
    glVertex( w, 0, 0 )
    glEnd()
    glBegin( GL_TRIANGLE_STRIP )
    glVertex( w, 0, 0 )
    glVertex( w, 0, l )
    glVertex( 0, 0, l )
    glVertex( w, 0, 0 )
    glVertex( 0, 0, 0 )
    glEnd()
    glBegin( GL_TRIANGLE_STRIP )
    glVertex( w, h, 0 )
    glVertex( w, h, l )
    glVertex( 0, h, l )
    glVertex( 0, h, 0 )
    glVertex( w, h, 0 )
    glEnd()
