"""
Author : Delaude Julien

Partie Graphique :
Source : https://github.com/h-nasir/PyQtChess/tree/284f5256cc594a4b2157984e7e0c23479410913b
"""
#!/usr/bin/env python3
# std
from os.path import isfile
from sys import argv

# local
from breakthrough import Breakthrough
from const import *
from errors import *
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from pyqt.menu import *
from pyqt.game import *

"""
MainWindow : Propose une Nouvelle Partie ou de quitter l'application
MenuFrame : Pop Up Menu 
GameFrame : Pop up tableau après choix du menu, non terminé
"""
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget(self)

        self.user = True

        # Instantiate frames for different pages
        self.main_menu = MenuFrame(self)
        self.game_frame = GameFrame(self)
        

        # Insert frames into a stack
        self.stack.insertWidget(0, self.main_menu)
        self.stack.insertWidget(1, self.game_frame)

        # Set current frame to main menu
        self.stack.setCurrentIndex(0)

        # Set window details
        self.setCentralWidget(self.stack)
        self.setWindowTitle("Breakthrough")
        self.setWindowIcon(QIcon("pawn_icon.png"))
        self.setMinimumSize(400, 250)
        self.show()
    def closeEvent(self, event):
        if self.user:
            if self.stack.currentIndex() == 1:
                save_prompt = QMessageBox()
                save_prompt.setWindowIcon(QIcon('pawn_icon.png'))
                save_prompt.setIcon(QMessageBox.Warning)
                save_prompt.setWindowTitle("BreakThrough")
                save_prompt.setText("Your current progress will be lost.")
                save_prompt.setInformativeText("Do you want to save the game?")
                save_prompt.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
                save_prompt.button(QMessageBox.Discard).setText("Quit out")
                option = save_prompt.exec_()

                if option == QMessageBox.Discard:
                    event.accept()
                # Cancel
                else:
                    event.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main(path=None):
    player2_is_ai = '-ai' in argv
    try:
        game = Breakthrough(path, player2_is_ai)
    except BadFormatError as e:
        print(e)
    else:
        game.play()
        winner = game.winner
        print(f'Player {CHARS[winner]} won!')

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window = Window()
    main()
    sys.exit(app.exec_())
    
