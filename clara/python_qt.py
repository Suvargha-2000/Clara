from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow
import sys

def window() :
   app = QApplication(sys.argv)
   win = QMainWindow()
   def change_text():
      label.setText('hi bois')
   win.setGeometry(0 , 0 , 300 , 300)
   win.setWindowTitle('New tutorial')
   label = QtWidgets.QLabel(win)
   label.setText('HHUHUHUH')
   label.move(50 , 50)
   b1 = QtWidgets.QPushButton(win)
   b1.setText('HHUHUHUH')
   b1.move(100 , 100)
   b1.clicked.connect(change_text)
   
   win.show()
   sys.exit(app.exec())

window()
