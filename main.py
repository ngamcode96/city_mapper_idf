from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from folium.plugins import Draw, MousePosition, MeasureControl
from branca.element import Element

from routes import *
from save_route import *

from get_data_from_db import *

import folium, io, json, sys, math, random, os

import psycopg2


class MyWindow(QMainWindow):

    RouteType = -1

    def open(self, from_stop, to_stop, RouteType):

        trips = getNetwork(from_stop, to_stop, self.RouteType)

        # self.window = QtWidgets.QMainWindow()
        self.ui = MainWindow()
        self.ui.from_box.addItem(from_stop)
        self.ui.to_box.addItem(to_stop)
        


        # self.ui.setupUi(self.window)

        for trip in trips:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setFamily("Sans Serif")
            font.setPointSize(12)
            item.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setBackground(brush)
            brush = QtGui.QBrush(QtGui.QColor(20, 85, 123))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setForeground(brush)

            station_details = trip.split(";")[1].split("*") 
            item.setText(station_details[0] + station_details[3]  )

            self.ui.listWidget.addItem(item)

            self.ui.webView.coordinates_form_stop.append(station_details[1])
            self.ui.webView.coordinates_form_stop.append(station_details[2])

            self.ui.webView.coordinates_to_stop.append(station_details[4])
            self.ui.webView.coordinates_to_stop.append(station_details[5])


        self.ui.listWidget.itemClicked.connect(lambda it,t=trips : self.affich(it, t))

        
        # self.window.show()
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200,200,300,300)
        self.resize(500, 500)
        self.setWindowTitle("Paris Mapper")
        self.setupUi(self)
    
    
    
    def getRoute(self):
        _fromstation = str(self.from_input.currentText())
        _tostation = str(self.to_input.currentText())

        self.open(_fromstation, _tostation, self.RouteType)

    
    def switch_station(self):

        _fromstation = str(self.from_input.currentText())
        _tostation = str(self.to_input.currentText())
        _tmp = _fromstation
        self.from_input.setEditText(_tostation)
        self.to_input.setEditText(_tmp)

    def get_stations(self):
        self.conn = psycopg2.connect(database="l3info_3", user="l3info_3", host="10.11.11.22", password="L3INFO_3")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""SELECT distinct name FROM station""")
        self.conn.commit()
        rows = self.cursor.fetchall()

        for row in rows : 
            self.from_input.addItem(str(row[0]))
            self.to_input.addItem(str(row[0]))

    def getRER(self):
        self.RouteType = 2
        self.button_Metro.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_RER.setStyleSheet("background:green; border-radius:10px;font-size:12px")
        self.button_Bus.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_All.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_Tram.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")

    
    def getMetro(self):
        self.RouteType = 1
        self.button_Metro.setStyleSheet("background:green; border-radius:10px;font-size:12px")
        self.button_RER.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_Bus.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_All.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_Tram.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")


    def getBus(self):
        self.RouteType = 3
        self.button_Metro.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_RER.setStyleSheet("background: #ffffff; border-radius:10px;font-size:12px")
        self.button_Bus.setStyleSheet("background:green; border-radius:10px;font-size:12px")
        self.button_All.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_Tram.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
    
    def getAll(self):
        self.RouteType = -1
        self.button_Metro.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_RER.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_Bus.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_All.setStyleSheet("background:green; border-radius:10px;font-size:12px")
        self.button_Tram.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")


    def getTram(self):
        self.RouteType = 0
        self.button_Metro.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_RER.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_Tram.setStyleSheet("background:green; border-radius:10px;font-size:12px")
        self.button_Bus.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        self.button_All.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")

    def saveStations(self,it, his, hist_name):
       from_station = self.from_input.currentText()
       to_station = self.to_input.currentText()

       result = save_to_database(from_station, to_station, hist_name)

       if(result == 1):
           print("SAVED INTO DATABASE")
           his.hide()
           self.open(from_station, to_station, -1)

    
    
    def addStations(self):

        self.histo = SaveHistoryWindow()
        self.histo._label_from.setText("From:"+self.from_input.currentText())
        self.histo._label_to.setText("To:"+self.to_input.currentText())

        hist_name = str(self.histo.history_name_box.currentText())
        self.histo.save_button.clicked.connect(lambda it,his = self.histo, h_name=hist_name : self.saveStations(it, his,h_name))

    def getHomeRoute(self):

        results = VerifyRouteInDatabase("Home")

        if(len(results) == 0):
            self.addStations()
        else:
            for stations in results:
                self.from_input.setEditText(stations[0])
                self.to_input.setEditText(stations[1])
                self.open(stations[0],stations[1],-1)
                

    def getUniversityRoute(self):
        
        results = VerifyRouteInDatabase("University")
        if(len(results) == 0):
            self.addStations()
        else:
            for stations in results:
                self.from_input.setEditText(stations[0])
                self.to_input.setEditText(stations[1])
                self.open(stations[0],stations[1],-1)
                

        
    def getWorkRoute(self):
        
        results = VerifyRouteInDatabase("Work")   
        if(len(results) == 0):
            self.addStations()
        else:
            for stations in results:
                self.from_input.setEditText(stations[0])
                self.to_input.setEditText(stations[1])
                self.open(stations[0],stations[1],-1)
                


    def affich(self, item, trips):
        trip_id=0
        for row in trips:
            trip=row.split(";")
            station_details = trip[1].split("*") 
            t = station_details[0] + station_details[3]

            if(t == item.text()):
                trip_id=trip[0]

        if ((trip_id!=0) & (trip[1]!= "No route available !")):
            trip=get_route(trip_id, self.from_input.currentText(), self.to_input.currentText())
            direction=trip.split(";")[0] 
            route_tab= trip.split(";")[1].split(",")
            # clear widget     
            self.ui.listWidget.clear()

            self.ui.button_direction.setText(direction)
            for row in route_tab:
                item = QtWidgets.QListWidgetItem()
                font = QtGui.QFont()
                font.setFamily("Sans Serif")
                font.setPointSize(12)
                item.setFont(font)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                item.setBackground(brush)
                brush = QtGui.QBrush(QtGui.QColor(20, 85, 123))
                brush.setStyle(QtCore.Qt.SolidPattern)
                item.setForeground(brush)
                item.setText(row)
                self.ui.listWidget.addItem(item)

            self.ui.mysplit.addWidget(self.ui.button_retour)
            self.ui.button_retour.clicked.connect(self.getRoute)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 522)
        MainWindow.setStyleSheet("background-color:#14557b")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setGeometry(QtCore.QRect(470, 110, 41, 31))
        self.go.setStyleSheet("background-color:#00273e; color:#ffffff;border-radius:10px")
        self.go.setObjectName("go")



        self.from_input = QtWidgets.QComboBox(self.centralwidget)
        self.from_input.setGeometry(QtCore.QRect(20, 110, 181, 31))
        self.from_input.setStyleSheet("background-color:#00273e; color:#ffffff;border-radius:10px")
        self.from_input.setObjectName("from_input")
        self.from_input.setEditable(True)


        self.to_input = QtWidgets.QComboBox(self.centralwidget)
        self.to_input.setGeometry(QtCore.QRect(280, 110, 181, 31))
        self.to_input.setStyleSheet("background-color:#00273e; color:#ffffff;border-radius:10px")
        self.to_input.setObjectName("to_input")
        self.to_input.setEditable(True)


        self.get_stations()


        self.btn_switch = QtWidgets.QPushButton(self.centralwidget)
        self.btn_switch.setGeometry(QtCore.QRect(220, 110, 41, 31))
        self.btn_switch.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_switch.setStyleSheet("border-radius:10px; background-color:#fff")
        self.btn_switch.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("mapper/images/arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_switch.setIcon(icon)
        self.btn_switch.setIconSize(QtCore.QSize(25, 25))
        self.btn_switch.setObjectName("btn_switch")
        self.button_home = QtWidgets.QPushButton(self.centralwidget)
        self.button_home.setGeometry(QtCore.QRect(20, 160, 101, 71))
        self.button_home.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("mapper/images/accueil.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_home.setIcon(icon1)
        self.button_home.setIconSize(QtCore.QSize(30, 30))
        self.button_home.setObjectName("pushButton")
        self.button_university = QtWidgets.QPushButton(self.centralwidget)
        self.button_university.setGeometry(QtCore.QRect(150, 160, 101, 71))
        self.button_university.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("mapper/images/universite (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_university.setIcon(icon2)
        self.button_university.setIconSize(QtCore.QSize(30, 30))
        self.button_university.setObjectName("button_university")
        self.button_work = QtWidgets.QPushButton(self.centralwidget)
        self.button_work.setGeometry(QtCore.QRect(280, 160, 101, 71))
        self.button_work.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("mapper/images/boy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_work.setIcon(icon3)
        self.button_work.setIconSize(QtCore.QSize(55, 55))
        self.button_work.setObjectName("button_work")
        self.button_add = QtWidgets.QPushButton(self.centralwidget)
        self.button_add.setGeometry(QtCore.QRect(410, 160, 101, 71))
        self.button_add.setStyleSheet("background:#ffffff; border-radius:10px; font-size:12px")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("mapper/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add.setIcon(icon4)
        self.button_add.setIconSize(QtCore.QSize(32, 32))
        self.button_add.setObjectName("button_add")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 260, 101, 17))
        self.label.setStyleSheet("color:#fff")
        self.label.setObjectName("label")
        self.button_RER = QtWidgets.QPushButton(self.centralwidget)
        self.button_RER.setGeometry(QtCore.QRect(30, 290, 71, 31))
        self.button_RER.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("mapper/images/subway.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_RER.setIcon(icon5)
        self.button_RER.setIconSize(QtCore.QSize(30, 30))
        self.button_RER.setObjectName("button_RER")


        self.button_Tram = QtWidgets.QPushButton(self.centralwidget)
        self.button_Tram.setGeometry(QtCore.QRect(190, 290, 81, 31))
        self.button_Tram.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("mapper/images/tram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_Tram.setIcon(icon6)
        self.button_Tram.setIconSize(QtCore.QSize(30, 30))
        self.button_Tram.setObjectName("button_Tram")
        self.button_Bus = QtWidgets.QPushButton(self.centralwidget)
        self.button_Bus.setGeometry(QtCore.QRect(280, 290, 91, 31))
        self.button_Bus.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("mapper/images/bus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_Bus.setIcon(icon7)
        self.button_Bus.setIconSize(QtCore.QSize(25, 25))
        self.button_Bus.setObjectName("button_Bus")
        self.button_All = QtWidgets.QPushButton(self.centralwidget)
        self.button_All.setGeometry(QtCore.QRect(380, 290, 91, 31))
        self.button_All.setStyleSheet("background:green; border-radius:10px;font-size:12px")
        self.button_All.setObjectName("button_All")
        self.button_Metro = QtWidgets.QPushButton(self.centralwidget)
        self.button_Metro.setGeometry(QtCore.QRect(110, 290, 71, 31))
        self.button_Metro.setStyleSheet("background:#ffffff; border-radius:10px;font-size:12px")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("mapper/images/m.pnfg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_Metro.setIcon(icon9)
        self.button_Metro.setIconSize(QtCore.QSize(25, 25))
        self.button_Metro.setObjectName("button_Metro")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 350, 81, 16))
        self.label_3.setStyleSheet("color:#fff")
        self.label_3.setObjectName("label_3")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(90, 350, 41, 21))
        self.pushButton_10.setStyleSheet("background-color:#14557b;border:none")
        self.pushButton_10.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("mapper/images/warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon10)
        self.pushButton_10.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_10.setObjectName("pushButton_10")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 380, 491, 81))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSpacing(4)

        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.go.setText(_translate("MainWindow", "GO"))
        self.from_input.setPlaceholderText(_translate("MainWindow", "Departure"))
        self.to_input.setPlaceholderText(_translate("MainWindow", "Arrivated"))
        self.button_home.setText(_translate("MainWindow", "Home"))
        self.button_university.setText(_translate("MainWindow", "University"))
        self.button_work.setText(_translate("MainWindow", "Work"))
        self.button_add.setText(_translate("MainWindow", "Add"))
        self.label.setText(_translate("MainWindow", "Travel Mode"))
        self.button_RER.setText(_translate("MainWindow", "RER"))
        self.button_Tram.setText(_translate("MainWindow", "Tram"))
        self.button_Bus.setText(_translate("MainWindow", "Bus"))
        self.button_All.setText(_translate("MainWindow", "Tous"))
        self.button_Metro.setText(_translate("MainWindow", "Metro"))
        self.label_3.setText(_translate("MainWindow", "Information"))

        disturbs = info_disturb()
        for disturb in disturbs:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setFamily("Sans Serif")
            font.setPointSize(12)
            item.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setBackground(brush)
            brush = QtGui.QBrush(QtGui.QColor(20, 85, 123))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setForeground(brush)
            item.setText(disturb)
            self.listWidget.addItem(item)

            
        self.go.clicked.connect(self.getRoute)

        self.button_RER.clicked.connect(self.getRER)
        self.button_Metro.clicked.connect(self.getMetro)
        self.button_Bus.clicked.connect(self.getBus)
        self.button_Tram.clicked.connect(self.getTram)
        self.button_All.clicked.connect(self.getAll)
        self.btn_switch.clicked.connect(self.switch_station)

        self.button_add.clicked.connect(self.addStations)
        self.button_home.clicked.connect(self.getHomeRoute)
        self.button_university.clicked.connect(self.getUniversityRoute)
        self.button_work.clicked.connect(self.getWorkRoute)

# class HistoryPopup(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)

#         self.controls_panel = QHBoxLayout()
#         self.controls_panel_1 = QHBoxLayout()
#         self._label = QLabel('From: ', self)
#         self._label.setFixedSize(30,20)
#         self._label.setGeometry(10,10,10,10)

#         self._label_from = QLabel('MASSY PALAISEAU',self)
#         self._label_from.setFixedSize(190,20)
#         self._label_from.setGeometry(10,30,10,10)
#         self._label_from.setStyleSheet("font-weight:bold")

#         self.from_box = QComboBox() 
#         self.from_box.setEditable(False)
#         self.controls_panel.addWidget(self._label_from)
#         self.controls_panel_1.addWidget(self.from_box)

#         self._label = QLabel('  To: ', self)
#         self._label.setFixedSize(20,20)
#         self._label.setGeometry(240,10,10,10)

#         self._label_to = QLabel("MASSY PALAISEAU", self)
#         self._label_to.setFixedSize(190,20)
#         self._label_to.setGeometry(250,30,10,10)
#         self._label_to.setStyleSheet("font-weight:bold")
#         self.to_box = QComboBox() 
#         self.to_box.setEditable(False)

#         self.controls_panel.addWidget(self._label)
#         self.controls_panel.addWidget(self._label_to)
#         self.controls_panel_1.addWidget(self.to_box)

#         self.go_button = QPushButton("Go!")
#         self.controls_panel_1.addWidget(self.go_button)

#         self.go_button = QPushButton("Go!")
#         self.controls_panel.addWidget(self.go_button)

#         self.save = QtWidgets.QPushButton()
#         self.save.setGeometry(120, 100, 10, 10)
#         self.save.setStyleSheet("background-color:#00273e; color:#000000;border-radius:10px")
#         self.save.setObjectName("save")
#         self.save.setText("Enregistrer")
#         self.controls_panel.addWidget(self.save)

#         types =["Home", "Work", "University", "Other"] 

#         self.history_name = QComboBox()
#         self.history_name.addItems(types)
#         self.history_name.setGeometry(50, 50, 50, 50)
#         self.controls_panel.addWidget(self.history_name)


#     # def paintEvent(self, e):
#     #     dc = QPainter(self)
#     #     dc.drawLine(0, 0, 100, 100)
#     #     dc.drawLine(100, 0, 0, 100)
    
def window():
    app = QApplication(sys.argv)
    window = MyWindow()
     
    window.show()
    sys.exit(app.exec_())

window()