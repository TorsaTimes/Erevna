from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTabWidget, QPushButton, QFileDialog, QTextEdit,  QLineEdit, QMainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QRunnable, QThreadPool, QObject, pyqtSignal, QRect, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QMovie
import time
import traceback, sys
import hashlib
from qtwidgets import PasswordEdit
import qtwidgets
import xml.etree.ElementTree as et
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(550, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet('''
        background-color:gray;
         QTabWidget::pane {             
             background-color: gray;
        }     
    ''')

        self.counter = 0
        self.n = 300 # total instance

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.labelTitle = QLabel(self)

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.setText('Erevna')
        self.labelTitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.labelTitle)
        self.labelTitle.setStyleSheet("""background: gray; font-family: Courier; color: white;                           
            font-size: 20pt;""")
        
        # add loading GIF
        self.label = QLabel(self)
        self.label.setGeometry(QRect(25, 25, 350, 250))
        self.label.setMinimumSize(QSize(350, 250))
        self.label.setMaximumSize(QSize(350, 250))
        self.label.resize(self.width() - 200 - 10, 50)
        self.label.move(100,  130)
        self.label.setAlignment(Qt.AlignCenter)

        # Loading the GIF
        self.movie = QMovie(resource_path("splashscreengif.gif"))
        self.label.setMovie(self.movie)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def loading(self):
        self.movie.start()
        if self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.myApp = MainWindow()
            self.myApp.show()

        self.counter += 1    

class MainWindow(QMainWindow):
    global data_list
    data_list = []


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.resize(False, False)
        self.setFixedSize(600, 700)
        self.setAcceptDrops(True)
        self.setWindowTitle('Erevna')
        self.setWindowIcon(QIcon(resource_path('icon.ico')))
        self.setStyleSheet("background-color: gray") 

        layout = QVBoxLayout()

        w = QWidget()
        w.setLayout(layout)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
        QTabWidget::pane {             
            border-width: 2px;         
            border-style: solid;       
            border-color: gray;         
            border-radius: 6px;
            height: 500px; 
            width: 600px;        
        }                              
        QTabBar {                                          
            background: gray;                         
            color: #ff000000;                              
            font-family: Courier;                          
            font-size: 12pt;                               
        }QTabBar::tab { 
            height: 60px; 
            width: 192px; 
            background: 'lightgray'; 
            color: black; 
            border-color: black;
        } 
        QTabBar::tab:selected,
        QTabBar::tab:hover 
        {
        border-top-color: gray;
        border-color: gray;
        color: black;
        background: gray; 
        }
        """) #289 qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #C1D8E8, stop: 1 #F0F5F8)
        
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tabs.addTab(tab1,"Drag n Drop")
        tabs.addTab(tab2,"Filesystem")
        tabs.addTab(tab3,"InputField")
        # tab2
        tab2.layout = QVBoxLayout(self)
        btn = QPushButton("PWD File")
        btn.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        btn.setFixedSize(600, 50)
        btn.clicked.connect(self.getfile)
        tab2.layout.addWidget(btn)
        tab2.layout.setAlignment(Qt.AlignCenter)
        tab2.setLayout(tab2.layout)
        # tab1
        tab1.layout = QVBoxLayout(self)
        photoViewer = ImageLabel()
        photoViewer.setStyleSheet("""border: 2px dashed gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        tab1.layout.addWidget(photoViewer)
        tab1.setLayout(tab1.layout)
        
        # tab3
        tab3.layout = QVBoxLayout(self)
        self.password = PasswordEdit()
        self.password.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        self.password.setFixedSize(570, 50)
        tab3.layout.addWidget(self.password)
        layout.setAlignment(self.password, Qt.AlignCenter)
        tab3.setLayout(tab3.layout)
        # add tab widget 
        layout.addWidget(tabs)
        ###### 

        # add loading GIF
        self.label = QLabel(self)
        self.label.setGeometry(QRect(25, 25, 350, 70))
        self.label.setMinimumSize(QSize(350, 70))
        self.label.setMaximumSize(QSize(350, 70))
        
        # Loading the GIF
        self.movie = QMovie(resource_path("b111.gif"))
        self.label.setMovie(self.movie)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)

        # Add Button
        check_btn = QPushButton("Check PWD")
        check_btn.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        check_btn.setFixedSize(580, 50)
        layout.addWidget(check_btn)
        layout.setAlignment(check_btn, Qt.AlignTop)
        check_btn.clicked.connect(self.startAnimation)
        self.r_label = QLabel("")
        layout.addWidget(self.r_label)
        layout.setAlignment(self.r_label, Qt.AlignCenter)
        self.r_label.setStyleSheet("""border: 1px solid gray; background: gray; font-family: Courier;                          
            font-size: 12pt;""")
        
        

        self.setCentralWidget(w)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def progress_fn(self, n):
        print("%d%% done" % n)

    # execute fnc 
    def search_pwd(self, progress_callback):
        list_of_pwds = data_list
        #n = 1
        for pwd in list_of_pwds:
            message_digest = hashlib.sha1()
            message_digest.update(bytes(pwd, encoding='utf-8'))
            to_check = message_digest.hexdigest().upper()

            leaked = False
            with open('sha1_hashes.txt') as file:
                for line in file:
                    if to_check in line:
                        self.r_label.setText('')
                        number = {line.split(':')[1].strip()}
                        self.r_label.setText('Your password has been leaked '+ str(number) +' times!')
                        leaked = True
                        self.stopAnimation()
                        break      
            if leaked == False:
                self.r_label.setText('Your password has not been leaked yet!')
                self.stopAnimation()
        data_list.clear()

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.search_pwd) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)



    def og_no_gif_start(self):
        # Pass the function to execute
        worker1 = Worker(self.startAnimation) # Any other args, kwargs are passed to the run function
        worker1.signals.result.connect(self.print_output)
        worker1.signals.finished.connect(self.thread_complete)
        worker1.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker1)

    # Get Data fnc
    #Drag and Drop Event Section
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        global data_list
        data_list.clear()
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            data_list =  self.get_data_from_file(file_path)
            event.accept()
        else:
            event.ignore()

    # input field
    def input_field(self):
        global data_list
        if (self.password.text()):
            data_list.clear()
            data_list.append(self.password.text())
            self.password.setText('')
    

    def get_data_from_file(self, filePath):
        list_val = []
        with open(filePath, 'r', encoding='utf-8') as f:
	        list_val = [_.rstrip('\n') for _ in f.readlines()]

        if not list_val:
            print(list_val, " Liste ist nicht voll ungleich true fehler ausgeben!!!")
        elif list_val: 
            print(list_val, " list ist voll und wird returned")
            return list_val
    
    #Get file from Explorer Section
    def getfile(self):
        global data_list
        data_list.clear()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            data_list = self.get_data_from_file(fileName) #schreib die daten in eine globale Liste

    # Start Animation
    def startAnimation(self):
        self.input_field()
        if not data_list:
            self.r_label.setText('Please Enter a Password')
            self.r_label.setStyleSheet("""border: 1px solid gray; color: red; background: gray; font-family: Courier;                          
            font-size: 12pt;""")

        elif data_list:
            self.r_label.setText('')
            self.r_label.setStyleSheet("""border: 1px solid gray; color: black; background: gray; font-family: Courier;                          
            font-size: 12pt;""")      
            self.label.setHidden(False)
            self.movie.start()
            self.oh_no()

          
    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()
        self.label.setHidden(True)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class ImageLabel(QLabel):
        def __init__(self, *args, **kwargs):
            super(ImageLabel, self).__init__(*args, **kwargs)
            self.setFixedSize(555,400)
            self.setAlignment(Qt.AlignCenter)
            self.setText('\n\n Drop File Here \n\n')
            self.setStyleSheet('''
                QLabel{
                    border: 4px dashed #aaa

                }
            ''')
if __name__ == '__main__':
    app = QApplication([])
    #window = MainWindow()
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
    #app.exec_()