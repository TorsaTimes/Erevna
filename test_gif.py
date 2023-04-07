import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
  
  
class LoadingGif(object):
  
    def mainUI(self, FrontWindow):
        FrontWindow.setObjectName("FTwindow")
        FrontWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(FrontWindow)
        self.centralwidget.setObjectName("main-widget")
        self.centralwidget.setStyleSheet('background: gray;')
  
        # Label Create
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 25, 500, 500))
        self.label.setMinimumSize(QtCore.QSize(500, 500))
        self.label.setMaximumSize(QtCore.QSize(500, 500))
        self.label.setObjectName("lb1")
        FrontWindow.setCentralWidget(self.centralwidget)
  
        # Loading the GIF
        self.movie = QMovie("l1.gif")
        self.label.setMovie(self.movie)
  
        #self.startAnimation()
  
    # Start Animation
    def startAnimation(self):
        self.movie.start()
  
    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()
  
  
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
demo = LoadingGif()
demo.mainUI(window)
window.show()
sys.exit(app.exec_())