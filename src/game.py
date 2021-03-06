from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from src.exceptions import *
from src.gameSprite import *
from src.geometry import *
from src.gameConst import *
import src.gameConst


class Game() :        

    def __init__( self ) :
        self.asteroids = []
        self.ship = Ship( ( 0, 0, GAME_Z ) )
        self.points = 0
        self.onPause = True
        self.gameOver = False

    def _generateAsteroids( self ) :
        n = self.points * DIFFICULTY - len( self.asteroids ) + 1
        self.currentAsteroidSize = 4 + self.points * ASTEROIDS_GROWN_RATIO
        src.gameConst.CURRENT_ASTEROID_QUALITY = MAX_ASTEROID_QUALITY - (
                                                 len( self.asteroids ) * ASTEROID_QUALITY_DEC )
        for i in range( 0, int(n) ) :
            self.asteroids.append( Asteroid( self.currentAsteroidSize ) )

    def update( self ) :
        if not self.onPause :
            self._generateAsteroids()
            for i in self.asteroids: i.update()
            self.ship.update()
            self.checkCollision()
        if AUTO_FIRE_MODE : self.ship.shoot()
        
    def checkCollision( self ) :
        for b in self.ship.usedBullets :
            if not b.isInBox() :
                self.ship.usedBullets.remove( b )
        for a in self.asteroids :
            if a.collide( self.ship ) :
                self.gameOver = True
                self.onPause = True
                break
            for b in self.ship.usedBullets :
                if not b.isDead and b.collide( a ) :
                    b.isDead = True
                    a.isDead = True
        for a in self.asteroids :
            if a.isDead :
                self.asteroids.remove( a )
                self.points += 1
                for na in a.split() :
                    self.asteroids.append( na )
        for b in self.ship.usedBullets :
            if b.isDead : self.ship.usedBullets.remove( b )
 
    def drawAll( self ) :
        for i in self.asteroids: i.blit()
        self.ship.blit()

    def restart( self ) :
        self.ship = Ship( ( 0, 0, GAME_Z ) )
        self.points = 0
        self.asteroids = []
        self.onPause = False
 
    def start( self ) :
        self.getGLReady()
        glutMainLoop()

    def pause( self ) :
        if self.onPause :
            self.onPause = False
            if self.gameOver :
                self.gameOver = False
                self.restart()
        else :
            self.onPause = True
    
    def getGLReady( self ) :
        self.setScreen()
        glClearColor( BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], 1 )
        glShadeModel( GL_SMOOTH )
        glEnable( GL_CULL_FACE )
        glEnable( GL_DEPTH_TEST )
        glPointSize( BULLET_SIZE )
        self.setLights()
        self.setGlutCallback()
        glMatrixMode( GL_PROJECTION )
        glOrtho( SCREEN.pos[0], SCREEN.pos[0]+SCREEN.w, 
                 SCREEN.pos[1], SCREEN.pos[1]+SCREEN.h,
                 NEAR_VAL, FAR_VAL )
        self.setCamera()

    def setGlutCallback( self ) :
        glutDisplayFunc( display )
        glutKeyboardFunc( keyPressed )
        glutMouseFunc( mouseClick )
        glutMotionFunc( mouseMotion )
        glutPassiveMotionFunc( mouseMotion )
        glutTimerFunc( BULLET_CHARGE_TIME,
                       clockTick,
                       BULLET_CHARGE_TIMER_VALUE )
    
    def setScreen( self ) :
        glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
        if FULLSCREEN_MODE :
            glutGameModeString( str(SCREEN.w) + "x" + str(SCREEN.h) + ":" + 
                                str(COLOR_DEPTH) + "@" + str(FPS) )
            glutEnterGameMode()
        else :
            glutInitWindowSize( SCREEN_SIZE[0], SCREEN_SIZE[1] )
            glutCreateWindow( FORM_NAME )

    def setLights( self ) :
        glEnable( GL_LIGHTING )
        glLightfv( GL_LIGHT0, GL_POSITION, LIGHT_0_POSITION )
        glLightfv( GL_LIGHT0, GL_DIFFUSE, LIGHT_0_COLOR )
        glLightf( GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1 )
        glLightf( GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05 )
        glEnable( GL_LIGHT0 )

    def setCamera( self ) :
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        gluLookAt( CAMERA_EYE[0], CAMERA_EYE[1], CAMERA_EYE[2], 
                   CAMERA_CENTER[0], CAMERA_CENTER[1], CAMERA_CENTER[2], 
                   0, 1, 0 )
        glPushMatrix()

gameController = Game()

def display() :
    gameController.update()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    gameController.drawAll()
    glutSwapBuffers()
    glutPostRedisplay()

def keyPressed( *args  ):
    if args[0] == '\x1b' : raise SystemExit
    if args[0] == 'w' or args[0] == 'W' : gameController.ship.turnUp()
    if args[0] == 's' or args[0] == 'S' : gameController.ship.turnDown()
    if args[0] == 'a' or args[0] == 'A' : gameController.ship.turnLeft()
    if args[0] == 'd' or args[0] == 'D' : gameController.ship.turnRight()
    if args[0] == ' ' : gameController.ship.shoot()
    if args[0] == 'p' or args[0] == 'P' : gameController.pause()
    if args[0] == 'r' or args[0] == 'R' : gameController.restart()

def mouseClick( button, state, x, y ) :
    gameController.ship.shoot()

def mouseMotion( x, y ) :
    gameController.ship.lastMousePos = x, y 

def clockTick( value ) :
    if value == BULLET_CHARGE_TIMER_VALUE :
        gameController.ship.shootCount += 1
        glutTimerFunc( BULLET_CHARGE_TIME,
                       clockTick,
                       BULLET_CHARGE_TIMER_VALUE )
