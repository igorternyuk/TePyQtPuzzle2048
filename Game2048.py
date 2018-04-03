from PyQt5.QtWidgets import QWidget, QFrame, QDesktopWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys, random
from math import*
from Model import*

TILE_SIZE = 100
FIELD_WIDTH = 4
FIELD_HEIGHT = 4
HALF_MARGIN = 10
GAME_INFO_PANEL_HEIGHT = 100
BUTTON_ROW_HEIGHT = 40

class MainWindow( QWidget ):
    def __init__( self ):
        super( MainWindow, self ).__init__()
        self.TITLE_OF_PROGRAM = "TePyQtPuzzle2048"
        self.init_UI()
        self.start_new_game( FIELD_WIDTH, FIELD_HEIGHT )

    def init_UI( self ):
        self.canvas = Canvas( self )
        self.canvas.setFixedSize( FIELD_WIDTH * TILE_SIZE + HALF_MARGIN,
         FIELD_HEIGHT * TILE_SIZE + HALF_MARGIN )
        self.btn3x3 = QPushButton( "3x3", self )
        self.btn3x3.clicked.connect( lambda : self.start_new_game(3, 3 ) )
        self.btn4x4 = QPushButton("4x4", self )
        self.btn4x4.clicked.connect(  lambda : self.start_new_game( 4, 4 ) )
        self.btn5x5 = QPushButton("5x5", self )
        self.btn5x5.clicked.connect(  lambda : self.start_new_game( 5, 5 )  )

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing( 0 )
        mainLayout.setContentsMargins( 0, 0, 0, 0 )

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins( 0, 0, 0, 0 )
        topLayout.addWidget( self.canvas, 0, Qt.AlignTop )

        bottomLayout = QHBoxLayout()
        bottomLayout.setSpacing( 5 )
        bottomLayout.addWidget( self.btn3x3 )
        bottomLayout.addWidget( self.btn4x4 )
        bottomLayout.addWidget( self.btn5x5 )

        mainLayout.addLayout( topLayout )
        mainLayout.addLayout( bottomLayout )
        self.setLayout( mainLayout )

        self.setWindowTitle( self.TITLE_OF_PROGRAM )
        self.setFixedSize( FIELD_WIDTH * TILE_SIZE + HALF_MARGIN,
         FIELD_HEIGHT * TILE_SIZE + GAME_INFO_PANEL_HEIGHT )
        self.centralize()
        self.show()

    def centralize( self ):
        screen = QDesktopWidget().screenGeometry()
        windowRect = self.geometry()
        dx = ( screen.width() - windowRect.width() ) / 2
        dy = ( screen.height() - windowRect.height() ) / 2
        self.move( dx, dy )

    def start_new_game( self, field_width, field_height ):
        self.model = Model( field_width, field_height, TILE_SIZE )
        self.model.reset()
        self.canvas.setFixedSize( self.model.field_width * TILE_SIZE + HALF_MARGIN,
          self.model.field_height * TILE_SIZE + GAME_INFO_PANEL_HEIGHT)
        self.setFixedSize( self.canvas.width(),
         self.canvas.height() + BUTTON_ROW_HEIGHT)
        self.update()
        self.centralize()

    def update_window_title( self ):
        self.setWindowTitle(self.TITLE_OF_PROGRAM + " Score: "
        + str( self.model.score ) + " Max: "+ str( self.model.max_tile_value ) )


class Canvas( QFrame ):
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.setFocusPolicy( Qt.StrongFocus )
        self.FONT = QFont( "Arial", 28 )
        self.COLOR_BACKGROUND = QColor( 157, 129, 111 )
        self.COLOR_EMPTY_SPOT = QColor( 178, 142, 119 )
        self.COLORS ={
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
        self.TIMER_DELAY = 50
        self.timer = QBasicTimer()
        self.timer.start( self.TIMER_DELAY, self )

    def keyReleaseEvent( self, event ):
        key = event.key()
        if key == Qt.Key_Space:
            self.parent().model.reset()
            self.update()
        elif key == Qt.Key_Right:
            self.parent().model.slide( Directions.RIGHT )
            self.update()
        elif key == Qt.Key_Left:
            self.parent().model.slide( Directions.LEFT )
            self.update()
        elif key == Qt.Key_Up:
            self.parent().model.slide( Directions.UP )
            self.update()
        elif key == Qt.Key_Down:
            self.parent().model.slide( Directions.DOWN )
            self.update()

    def timerEvent( self, event ):
        if event.timerId() == self.timer.timerId():
            self.parent().model.tick()
            self.update()

    def paintEvent( self, event ):
        painter = QPainter( self )
        self.render_empty_field( painter )
        self.render_tiles( painter )
        self.render_game_state( painter )
        self.render_game_info( painter )
        self.parent().update_window_title()

    def render_tiles( self, painter ):
        for tile in self.parent().model.tiles:
            if tile.is_sliding():
                self.render_tile( painter, tile )
        for tile in self.parent().model.tiles:
            if not tile.is_sliding():
                self.render_tile( painter, tile )

    def render_tile( self, painter, tile ):
        painter.setFont( self.FONT )
        if tile.value != 0:
            color = QColor( self.COLORS[tile.value] )
            painter.setBrush( color )
            painter.fillRect( tile.x + HALF_MARGIN, tile.y + HALF_MARGIN,
             TILE_SIZE - HALF_MARGIN, TILE_SIZE - HALF_MARGIN, color )
            painter.setPen( QPen( QColor( 50, 50, 50 ), 5 ) )
            painter.drawText( QRectF( tile.x + HALF_MARGIN, tile.y + HALF_MARGIN,
             TILE_SIZE - HALF_MARGIN, TILE_SIZE - HALF_MARGIN ),
             Qt.AlignCenter | Qt.AlignTop, str( tile.value ) )

    def render_game_info( self, painter ):
        font = QFont("Arial", 28 if self.parent().model.field_width == 4
        or self.parent().model.field_width == 5 else 14 )
        painter.setFont( font )
        max_val = self.parent().model.max_tile_value
        score = self.parent().model.score
        color = QColor( self.COLORS[max_val] ) if self.parent().model.max_tile_value != 64 else Qt.black
        painter.setPen( QPen( color, 7 ) )
        text = "Score: " + str( score ) + " Max: " + str( max_val )
        painter.drawText( QRectF( 0, self.height() - GAME_INFO_PANEL_HEIGHT,
         self.width(), GAME_INFO_PANEL_HEIGHT ), Qt.AlignCenter | Qt.AlignTop, text)

    def render_game_state( self, painter ):
        font = QFont( "Arial", 40 )
        painter.setFont( font )
        text = ""
        if self.parent().model.game_state == GameState.VICTORY:
            painter.setPen( QPen( QColor( 0, 190, 0 ), 60 ) )
            text = "YOU WON!!!"
        elif self.parent().model.game_state == GameState.DEFEAT:
            painter.setPen( QPen( QColor( 255, 0, 0 ), 60 ) )
            text = "YOU LOST!!!"
        painter.drawText( QRectF( 0, 0, self.parent().model.field_width * TILE_SIZE,
         self.parent().model.field_height * TILE_SIZE ), Qt.AlignCenter | Qt.AlignTop, text)

    def render_empty_field( self, painter ):
        height = self.height() - GAME_INFO_PANEL_HEIGHT + HALF_MARGIN
        painter.fillRect( 0, 0, self.width(), height, self.COLOR_BACKGROUND )
        for i in range( self.parent().model.field_height ):
            for j in range ( self.parent().model.field_width ):
                painter.fillRect( j * TILE_SIZE + HALF_MARGIN,
                 i * TILE_SIZE + HALF_MARGIN, TILE_SIZE - HALF_MARGIN,
                  TILE_SIZE - HALF_MARGIN, self.COLOR_EMPTY_SPOT )


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
