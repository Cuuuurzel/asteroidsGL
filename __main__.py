import sys
version = str( sys.version_info[0] ) + str( sys.version_info[1] )
if version != "27" :
    sys.stderr.write( "Python 2.7 and PyOpenGL are needed!!\n" )
    exit( 1 )
from src.game import *

if __name__ == "__main__"  :
    gameController.start()
