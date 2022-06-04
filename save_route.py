import folium, io, json, sys, math, random, os
import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from folium.plugins import Draw, MousePosition, MeasureControl
from jinja2 import Template
from branca.element import Element
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class SaveHistoryWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(520, 522)
        self.setStyleSheet("background:#14557b")
        self.setWindowTitle("Add History ")


	
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)



       
        self.button_direction = QtWidgets.QPushButton()
        self.button_direction.setGeometry(QtCore.QRect(10, 80, 41, 40))
        self.button_direction.setStyleSheet("background-color:#001478; color:#ffffff ;border-radius:7px; font-size:16px")
        self.button_direction.setObjectName("button_direction")
        self.button_direction.setText("ROUTES")

		
        controls_panel = QHBoxLayout()
        controls_panel_1 = QHBoxLayout()
        self.mysplit = QSplitter(Qt.Vertical)
        # self.mysplit.addWidget(self.button_direction)

        main.layout().addLayout(controls_panel)
        main.layout().addLayout(controls_panel_1)
        main.layout().addWidget(self.mysplit)

        self._label_from = QLabel('From: MASSY PALAISEAU', self)
        self._label_from.setFixedSize(250,20)
        self._label_from.setStyleSheet("color:#ffffff; font-weight:bold")
        self._label_from.setGeometry(10,10,10,10)

        _label_1 = QLabel('Name of history:', self)
        _label_1.setFixedSize(130,20)
        _label_1.setStyleSheet("color:#ffffff; font-weight:bold")
        # _label_1.setGeometry(10,10,10,10)

        types =["Home", "Work", "University", "Other"] 
        self.history_name_box = QComboBox()
        self.history_name_box.addItems(types)
        controls_panel_1.addWidget(_label_1)
        controls_panel_1.addWidget(self.history_name_box)
        controls_panel.addWidget(self._label_from)


        self._label_to = QLabel('  To: PARIS NORD', self)
        self._label_to.setFixedSize(240,20)
        self._label_to.setStyleSheet("color:#ffffff; font-weight:bold")

        self.save_button = QPushButton("Save history")

        controls_panel.addWidget(self._label_to)
        controls_panel_1.addWidget(self.save_button)

        # self.save_button.clicked.connect(self.save_to_database)
        self.startingpoint = True
                   
        self.show()
            

    


       
			
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = SaveHistoryWindow()
    window.show()
    sys.exit(app.exec_())
