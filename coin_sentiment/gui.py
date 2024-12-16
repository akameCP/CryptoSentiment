
from PyQt5.QtWidgets import QTextEdit, QMainWindow, QVBoxLayout, QWidget, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QMdiArea, QDockWidget
from PyQt5.QtGui import QPainter ,QColor
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from rscarp import NewsData
from btcdata import BtcGraphData
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

import asyncio

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Kullanici Girisi')
        self.setGeometry(200, 200, 300, 150)
        
        self.label_username = QLabel('Kullanici Adi:', self)
        self.label_username.move(20,20)
        
        self.label_password = QLabel('Şifre:', self)
        self.label_password.move(20,60)
        
        self.input_username = QLineEdit(self)
        self.input_username.move(120,20)
        
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit().Password)
        self.input_password.move(120,60)
        
        self.label_pushbutton = QPushButton('Giriş Yapin', self)
        self.label_pushbutton.move(20,100)
        self.label_pushbutton.clicked.connect(self.check_login)
        
        
        
    def check_login(self):
        username = self.input_username.text()
        password = self.input_password.text()
        if username == 'root' and password == 'kali':
            self.home_page = HomePage()
            self.home_page.show()
            self.close()
        else:
            label_messagebox = QMessageBox()
            label_messagebox.setWindowTitle('Hatali Giris')
            label_messagebox.setText('Hatali giris bilgileri !')
            label_messagebox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            label_messagebox.exec_()
            
        
        
class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mdi = QMdiArea()
        self.setWindowTitle('Botullah')
        self.setCentralWidget(self.mdi)
        
        self.setDock = QDockWidget('New')
        
        bar = self.menuBar()
        file = bar.addMenu('File')
        file.addAction('New')
        file.addAction('Btc')
        file.addAction('Graph')
        self.docPanel()
        
        
    def docPanel(self):
        #setDockWidgetright = QWidget()
        
        self.setGeometry(200, 200, 600, 400)
        setDockWidgetleft = QWidget()
        layout = QVBoxLayout(setDockWidgetleft) 
        
        
        button_news = QPushButton('News',setDockWidgetleft)
        button_chart = QPushButton('NewsChart',setDockWidgetleft)
        button_btc_chart = QPushButton('BtcChart',setDockWidgetleft)
        

        layout.addWidget(button_news)
        layout.addWidget(button_btc_chart)
        layout.addWidget(button_chart)
        

        
        setDockWidgetbottom = QWidget()
        dock_widgetleft = QDockWidget('Sabit Pencere', self)
        dock_widgetbottom = QDockWidget('Sabit Pencere', self)
        
        dock_widgetleft.setWidget(setDockWidgetleft)
        dock_widgetbottom.setWidget(setDockWidgetbottom)
        
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widgetleft)
        #self.addDockWidget(Qt.RightDockWidgetArea, dock_widgetright)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_widgetbottom)
        
        dock_widgetleft.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock_widgetbottom.setFeatures(QDockWidget.NoDockWidgetFeatures)
        # tıklama etkinlikleri
        button_chart.clicked.connect(self.open_chart)
        button_news.clicked.connect(self.open_news_text)
        button_btc_chart.clicked.connect(self.open_btc_chart)
        
        
        self.chart_bitcoin = PieChartBitcoin()
        self.news_text = NewsText()
        self.btc_chart = BtcChart()
        
        self.timer = QTimer(self)
        self.start_data_loader()
        self.timer.timeout.connect(self.start_data_loader)
        self.timer.start(30000)
        
        
    def start_data_loader(self):
        
            self.data_loader = DataLoader() 
            
            self.data_loader.pie_signal.connect(self.show_pie_chart)
            self.data_loader.news_signal.connect(self.show_news_text)
            self.data_loader.btc_data_signal.connect(self.show_btc_chart)
            self.data_loader.start()
        
            

        
    def show_pie_chart(self,pos,neg,neu,comp):
        self.chart_bitcoin.pie_chart(pos,neg,neu,comp)
    
    def show_news_text(self,text):
        self.news_text.news_text(text)
        
    def show_btc_chart(self,data):
        self.btc_chart.btc_chart(data)
        
        
    def open_chart(self):
        self.chart_bitcoin.show()
        
    def open_news_text(self):
        self.news_text.show()
    
    def open_btc_chart(self):
        self.btc_chart.show()
 

       
        
class NewsText(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 600, 400)
        self.label = QTextEdit('loading...',self)
        self.label.setReadOnly(True)
        self.label.setFixedSize(1000,800)
        self.label.move(20,20)
        
    def news_text(self,text):
        self.label.setReadOnly(False)
        self.label.setPlainText(str(text))
        self.label.setReadOnly(True)
        
class PieChartBitcoin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Chart")
        self.setGeometry(200, 200, 600, 400)
        
        self.page_chart = QWidget(self)
        self.layout = QVBoxLayout(self.page_chart)
        
        self.label = QLabel("Bitcoin Price Chart", self.page_chart)
        self.label.setFixedSize(100,25)
        self.layout.addWidget(self.label)
        
        self.label_chartsdata = QLabel('loading...',self)
        self.label_chartsdata.setFixedSize(100,25)
        self.layout.addWidget(self.label_chartsdata)
        ####
        self.pie_chart_load = PieChartLoad()
        self.layout.addWidget(self.pie_chart_load)
       # self.pie_chart_load.setVisible(False)
        self.setCentralWidget(self.page_chart)
        
        
        #########if page_chart.isVisible():
        #self.update_data_chart()
        

            
        #self.setCentralWidget(page_chart)
        
    def pie_chart(self,pos,neg,neu,comp):
        self.label_chartsdata.setText('pos = '+str(pos)+' neg = '+str(neg))
        y=np.array([pos,neg,neu])
        self.pie_chart_load.pie_chart_loader(y)
        print(pos,neg)
        #self.pie_chart_load.setVisible(True)
        
class BtcChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle('BtcChart')
        page_chart = QWidget(self)
        layout = QVBoxLayout(page_chart)
        
        self.btc_chart_load = BtcChartLoad()
        layout.addWidget(self.btc_chart_load)
        self.setCentralWidget(page_chart)
        
    def btc_chart(self,data):
        self.btc_chart_load.btc_chart_loader(data)
    
    
        
class DataLoader(QThread):
    signal = pyqtSignal(str)
    pie_signal = pyqtSignal(int, int, int, int)
    news_signal = pyqtSignal(str)
    btc_data_signal = pyqtSignal(np.ndarray)
    #kalman_data_signal = pyqtSignal(np.ndarray)
    
    def run(self):
        asyncio.run(self.data_loading())
        
    async def data_loading(self):
        await asyncio.sleep(1)
        news_data = NewsData()
        btc_graph_data = BtcGraphData()
        
        data, pos, neu, neg ,news = news_data.run()
        set_btc_graph_data = btc_graph_data.run()
        
        
        self.signal.emit(str(data))
        self.pie_signal.emit(int(pos*100), int(neg*100), int(neu*100), int(data*100))
        self.news_signal.emit(str(news))
        self.btc_data_signal.emit(set_btc_graph_data)
        #self.kalman_data_signal.emit(np.array(kalman_data)[-1])
        
class PieChartLoad(FigureCanvas):
    def __init__(self):
        self.fig = Figure(facecolor='white') 
        self.ax = self.fig.add_subplot(111)  
        super().__init__(self.fig)  
        
    def pie_chart_loader(self, data):
        mylabels = ['pos', 'neg', 'neu']
        mycolors = ["c", "r", "#808080"]

        self.ax.clear()  
        self.ax.pie(data, labels=None, autopct='', startangle=90, colors=mycolors)
        self.ax.set_title("Sentiment Analysis Pie Chart")
        self.ax.legend(mylabels, title="Sentiment", loc="upper right")
        self.draw()  
        

class BtcChartLoad(FigureCanvas):
    def __init__(self):
        self.fig = Figure(facecolor='white')
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        
    def btc_chart_loader(self, data):


        self.ax.clear()  
        self.ax.plot(data)
        self.ax.set_title("Bitcoin chart")
        self.draw()          

        
    #def paintEvent(self, event):
    #    qp = QPainter()
    #    qp.begin(self)
     #   qp.setPen(QColor(0, 0, 255))
    #    qp.drawRect(100,100,300,300)
    #    qp.end()
    
  
        




    