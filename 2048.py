from PyQt5.QtWidgets import QWidget, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys, random
from math import*
from Model import*

TITLE_OF_PROGRAM = "TePyQtPuzzle2048"
TILE_SIZE = 100
FIELD_WIDTH = 4
FIELD_HEIGHT = 4
TIMER_DELAY = 50
GAME_INFO_PANEL_HEIGHT = 55
WINDOW_WIDTH = FIELD_WIDTH * TILE_SIZE + 5
WINDOW_HEIGHT = FIELD_HEIGHT * TILE_SIZE + GAME_INFO_PANEL_HEIGHT

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

"""
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.button = QPushButton('Test', self)
        self.label = QLabel(self)
        self.button.clicked.connect(self.handleButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
"""

class MainWindow( QWidget ):
    def __init__( self ):
        super( MainWindow, self ).__init__()
        self.init_UI()

    def init_UI( self ):
        self.canvas = Canvas( self )
        self.canvas.setFixedSize( WINDOW_WIDTH, FIELD_HEIGHT * TILE_SIZE + 5 )
        self.btn3x3 = QPushButton( "3x3", self )
        #self.btn3x3.clicked.connect( self.canvas.start_new_game3x3 )
        self.btn4x4 = QPushButton("4x4", self )
        self.btn5x5 = QPushButton("5x5", self )
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing( 0 )
        mainLayout.setContentsMargins( 0, 0, 0, 0 )
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins( 0, 0, 0, 0 )
        topLayout.addWidget( self.canvas, 0, Qt.AlignTop )
        bottomLayout = QHBoxLayout()

        bottomLayout.addWidget( self.btn3x3 )
        bottomLayout.addWidget( self.btn4x4 )
        bottomLayout.addWidget( self.btn5x5 )

        mainLayout.addLayout( topLayout )
        mainLayout.addLayout( bottomLayout )
        self.setLayout( mainLayout )

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
        self.model = Model( FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE )
        self.model.reset()
        self.setFocusPolicy( Qt.StrongFocus )
        self.timer = QBasicTimer()
        self.timer.start( TIMER_DELAY, self )
        self.HALF_MARGIN = 5

    def start_new_game3x3( self ):
        self.model = Model( 3, 3, TILE_SIZE )
        self.model.reset()
        self.parent.setFixedSize( 3 * TILE_SIZE + 100, 3 * TILE_SIZE )

    def keyReleaseEvent( self, event ):
        key = event.key()
        if key == Qt.Key_Space:
            self.model.reset()
            self.update()
        elif key == Qt.Key_Right:
            self.model.slide( Directions.RIGHT )
            self.update()
        elif key == Qt.Key_Left:
            self.model.slide( Directions.LEFT )
            self.update()
        elif key == Qt.Key_Up:
            self.model.slide( Directions.UP )
            self.update()
        elif key == Qt.Key_Down:
            self.model.slide( Directions.DOWN )
            self.update()

    def timerEvent( self, event ):
        if event.timerId() == self.timer.timerId():
            self.model.tick()
            self.update()

    def paintEvent( self, event ):
        painter = QPainter( self )
        painter.setFont( FONT )
        self.render_empty_field( painter )
        for tile in self.model.tiles:
            if tile.is_sliding():
                self.render_tile( painter, tile )
        for tile in self.model.tiles:
            if not tile.is_sliding():
                self.render_tile( painter, tile )
        self.parent().setWindowTitle(TITLE_OF_PROGRAM + " Score: "
        + str( self.model.score ) + " Max: "+ str( self.model.max_tile_value ) )
        font = QFont( "Arial" )
        font.setPointSize( 80 )
        text = ""
        if self.model.game_state == GameState.VICTORY:
            painter.setPen( QPen( QColor( 0, 190, 0 ), 20 ) )
            text = "YOU WON!!!"
        elif self.model.game_state == GameState.DEFEAT:
            painter.setPen( QPen( QColor( 255, 0, 0 ), 20 ) )
            text = "YOU LOST!!!"
        painter.drawText( QRectF( 0, 0, FIELD_WIDTH * TILE_SIZE, FIELD_HEIGHT *
         TILE_SIZE ), Qt.AlignCenter | Qt.AlignTop, text)


    def render_empty_field( self, painter ):
        painter.fillRect( 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Qt.gray )
        for i in range( self.model.field_height ):
            for j in range ( self.model.field_width ):
                painter.fillRect( j * TILE_SIZE + self.HALF_MARGIN,
                 i * TILE_SIZE + self.HALF_MARGIN, TILE_SIZE - self.HALF_MARGIN,
                  TILE_SIZE - self.HALF_MARGIN, QColor( 100, 100, 100))

    def render_tile( self, painter, tile ):
        if tile.value != 0:
            color = QColor( COLORS[tile.value] )
            painter.setBrush( color )
            painter.fillRect( tile.x + self.HALF_MARGIN, tile.y + self.HALF_MARGIN,
             TILE_SIZE - self.HALF_MARGIN, TILE_SIZE - self.HALF_MARGIN, color )
            painter.setPen( QPen( QColor( 50, 50, 50 ), 5 ) )
            painter.drawText( QRectF( tile.x, tile.y, TILE_SIZE, TILE_SIZE ),
             Qt.AlignCenter | Qt.AlignTop, str( tile.value ) )

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
