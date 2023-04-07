import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTabWidget, QPushButton, QFileDialog, QTextEdit,  QLineEdit, QMainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QRunnable, QThreadPool
from PyQt5.QtGui import QPixmap, QIcon
from pdf2image import convert_from_path
from read_img import  extract_file
from qtwidgets import PasswordEdit
#from search_user_pwd import search_pwd
import hashlib

def search_pwd(pwd_var):
    list_of_pwds = pwd_var
    for pwd in list_of_pwds:
        message_digest = hashlib.sha1()
        message_digest.update(bytes(pwd, encoding='utf-8'))
        to_check = message_digest.hexdigest().upper()

        leaked = False
        with open('sha1_hashes.txt') as file:
            for line in file:
                if to_check in line:
                    print(f'Dein Paswort wurde', {line.split(':')[1].strip()}, 'mal geleaked!')
                    leaked = True
                    break
                #if not leaked:           
            if not leaked:
                print('Dein Passwort wurde noch nicht geleaked!')

def remove_file(f):
    print("WARUM" + " " + f)
    if os.path.exists(f):
        print("exist")
        os.remove(f)
    else:
        print("gibts nicht ")

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
    
    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(555,400)
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa

            }
        ''')

class MainWindow(QMainWindow):
    global data_list
    data_list = []
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
    # def __init__(self, parent=None):
    
    #     super(MainWindow, self).__init__(parent)
        self.central_widget = AppDemo(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: gray") 
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.show()
        # self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        # self.resize(False, False)
        # self.setFixedSize(600, 700)
        # self.setAcceptDrops(True)
        # self.setWindowTitle('Erevna')
        # self.setWindowIcon(QIcon('icon.png'))
        # self.setStyleSheet("background-color: gray") 
        # self.show()
        # layout = QVBoxLayout()
        # # self.setLayout(mainLayout)
        # w = QWidget()
        # w.setLayout(layout)
        # layout.addWidget(self.w)

class AppDemo(QWidget):
    global data_list
    data_list = []
    # def __init__(self):
    #     super().__init__()
    def __init__(self, parent):        
        super(AppDemo, self).__init__(parent)
       
        self.resize(False, False)
        self.setFixedSize(600, 700)
        self.setAcceptDrops(True)
        self.setWindowTitle('Erevna')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: gray")
        

        # self.setLayout(mainLayout)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
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
        }""") #289 qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #C1D8E8, stop: 1 #F0F5F8)
        
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        #self.tab1.resize(100,100)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Drag n Drop")
        self.tabs.addTab(self.tab2,"Filesystem")
        self.tabs.addTab(self.tab3,"InputField")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.photoViewer = ImageLabel()
        self.photoViewer.setStyleSheet("""border: 2px dashed gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        self.tab1.layout.addWidget(self.photoViewer)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.btn = QPushButton("PWD File")
        self.btn.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        self.btn.setFixedSize(600, 50)
        self.btn.clicked.connect(self.getfile)
        self.tab2.layout.addWidget(self.btn)
        self.tab2.layout.setAlignment(Qt.AlignCenter)
		
        #self.tab2.layout.addWidget(self.btn)
        self.tab2.setLayout(self.tab2.layout)

        # Create third tab
        self.tab3.layout = QVBoxLayout(self)
        # self.e1 = QLineEdit("Enter Password")
        # self.e1.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
        #     font-size: 20pt;""")
        # self.e1.setFixedSize(600, 50)
        # self.e1.setEchoMode(QLineEdit.Password)
        # self.tab3.layout.addWidget(self.e1)
        # self.layout.setAlignment(self.e1, Qt.AlignCenter)     
        self.password = PasswordEdit()
        self.password.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        self.password.setFixedSize(570, 50)
        self.tab3.layout.addWidget(self.password)
        self.layout.setAlignment(self.password, Qt.AlignCenter)
        self.tab3.setLayout(self.tab3.layout)

        

        # # Add tabs to widget
        self.layout.addWidget(self.tabs)

        # Add Button
        self.check_btn = QPushButton("Check PWD")
        self.check_btn.setStyleSheet("""border: 1px solid gray; background: lightgray; font-family: Courier;                          
            font-size: 20pt;""")
        self.check_btn.setFixedSize(580, 50)
        self.layout.addWidget(self.check_btn)
        self.layout.setAlignment(self.check_btn, Qt.AlignTop)
        self.check_btn.clicked.connect(self.start_pwd_check)
        self.label = QLabel("""Result: awdwadwadwbivfgurabguibirlgbhirdölgbuiarepöbgaödbgfvuagerbprögvbdiujgbuierdbgvfjygbyudisgfbduoy
        bvdfybvuidfbfgou<dsbviudbysigvubdfyvgubyfdub""")
        self.layout.addWidget(self.label)

    #Get file from Explorer Section
    def getfile(self):
        global data_list
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 
        'c:\\',"Image files (*.jpg *.gif *.png *.pdf *.txt)")
        # string_var = extract_file(fname)
        # print(string_var)
        data_list = self.get_data_from_file(fname) #schreib die daten in eine globale Liste



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
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            data_list =  self.get_data_from_file(file_path)
            #string_var = extract_file(file_path)
            #print(string_var, " string_var daasdasd")
            #remove_file(file_path)
            event.accept()
        else:
            event.ignore()

    def input_field(self):
        print(self.password.text())
        self.password.setText('Enter Password')
        #self.password.PasswordEdit(show_visibility=False)
        self.password.setEchoMode()
    

    def get_data_from_file(self, filePath):
        list_val = []
        with open(filePath, 'r', encoding='utf-8') as f:
	        list_val = [_.rstrip('\n') for _ in f.readlines()]

        if not list_val:
            print(list_val, " Liste ist nicht voll ungleich true fehler ausgeben!!!")
        elif list_val: 
            print(list_val, " list ist voll und wird returned")
            return list_val

    def start_pwd_check(self):
        worker = Worker(search_pwd(data_list))
        self.threadpool.start(worker)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")    
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


# app = QApplication(sys.argv)
# demo = AppDemo()
# demo.show()
app = QApplication([])
window = MainWindow()
sys.exit(app.exec_())