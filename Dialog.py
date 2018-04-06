from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from Model import*

class Dialog( QDialog ):
    def __init__(self, main_window, parent=None):
        super().__init__( parent )
        self.main_window = main_window
        msgBox = QMessageBox()
        btn_keep_going = QPushButton('Keep going')
        btn_keep_going.clicked.connect( self.keep_going )
        btn_new_game = QPushButton('New game')
        btn_new_game.clicked.connect( self.start_new_game )
        btn_exit = QPushButton('Exit')
        btn_exit.clicked.connect( lambda : self.main_window.close() )
        msgBox.setText('Congratulations!!!What would you like to do?')
        msgBox.addButton( btn_keep_going, QMessageBox.YesRole)
        msgBox.addButton( btn_new_game, QMessageBox.NoRole)
        msgBox.addButton( btn_exit, QMessageBox.RejectRole)
        ret = msgBox.exec_()

    def keep_going( self ):
        self.main_window.model.game_state = GameState.PLAYING_AFTER_2048

    def start_new_game( self ):
        self.main_window.model.reset()
        self.main_window.canvas.update()
