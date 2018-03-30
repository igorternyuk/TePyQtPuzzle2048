from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
import sys, random
from math import*
from Model import*

TITLE_OF_PROGRAM = "TePyQtPuzzle2048"
TILE_SIZE = 100
FIELD_WIDTH = 4
FIELD_HEIGHT = 4
WINDOW_WIDTH = FIELD_WIDTH * TILE_SIZE
WINDOW_HEIGHT = FIELD_HEIGHT * TILE_SIZE

COLORS ={
0:'#2c3e50',
2:'#1abc9c',
4:'#2ecc71',
8:'#27ae60',
16:'#3498db',
32:'#9b59b6',
64:'#f1c40f',
128:'#f39c12',
256:'#e67e22',
512:'#d35400',
1024:'#e74c3c',
2048:'#c0392b'
}

FONT = QFont( "Arial", 28 )
#FONT_SIZE = 40

def get_font_size_by_tile_value( value ):
    return log2( value )

class MainWindow( QMainWindow ):
    def __init__( self ):
        super().__init__()
        self.init_UI()

    def init_UI( self ):
        self.canvas = Canvas( self )
        self.setCentralWidget( self.canvas )
        self.setWindowTitle( TITLE_OF_PROGRAM )
        self.setFixedSize( WINDOW_WIDTH, WINDOW_HEIGHT )
        self.centralize()
        self.show()

    def centralize( self ):
        screen = QDesktopWidget().screenGeometry()
        windowRect = self.geometry()
        dx = ( screen.width() - windowRect.width() ) / 2
        dy = ( screen.height() - windowRect.height() ) / 2
        self.move( dx, dy )


class Canvas( QFrame ):
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.setFocusPolicy( Qt.StrongFocus )
        self.model = Model( FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE )

    def keyReleaseEvent( self, event ):
        key = event.key()
        if key == Qt.Key_Space:
            self.model.slide()
            self.update()

    def timerEvent( self, event ):
        pass

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setFont( FONT )
        for line in self.model.grid:
            for tile in line:
                if tile.value != 0:
                    color = QColor( COLORS[tile.value] )
                    painter.setBrush( color )
                    painter.fillRect( tile.x + 2, tile.y + 2, TILE_SIZE - 2, TILE_SIZE - 2, color )
                    painter.setPen( QPen( QColor( 50, 50, 50 ), 5 ) )
                    painter.drawText( QRectF( tile.x, tile.y, TILE_SIZE, TILE_SIZE ),
                     Qt.AlignCenter | Qt.AlignTop, str( tile.value ) )

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
