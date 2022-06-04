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



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(520, 522)
        self.setStyleSheet("background:#14557b")
        self.setWindowTitle("ROUTE ")


	
        main = QWidget()
        self.setCentralWidget(main)
        main.setLayout(QVBoxLayout())
        main.setFocusPolicy(Qt.StrongFocus)



        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setGeometry(QtCore.QRect(10, 210, 581, 301))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSpacing(4)

        self.button_direction = QtWidgets.QPushButton()
        self.button_direction.setGeometry(QtCore.QRect(10, 80, 41, 40))
        self.button_direction.setStyleSheet("background-color:#001478; color:#ffffff ;border-radius:7px; font-size:16px")
        self.button_direction.setObjectName("button_direction")
        self.button_direction.setText("ROUTES")

        self.button_retour = QtWidgets.QPushButton()
        self.button_retour.setGeometry(QtCore.QRect(10, 80, 41, 40))
        self.button_retour.setStyleSheet("background-color:#001478; color:#ffffff ;border-radius:7px; font-size:16px")
        self.button_retour.setObjectName("button_retour")
        self.button_retour.setText("RETOUR")


        self.webView = myWebView()


		
        controls_panel = QHBoxLayout()
        self.mysplit = QSplitter(Qt.Vertical)
        self.mysplit.addWidget(self.webView)
        self.mysplit.addWidget(self.button_direction)
        self.mysplit.addWidget(self.listWidget)

        main.layout().addLayout(controls_panel)
        main.layout().addWidget(self.mysplit)

        _label = QLabel('From: ', self)
        _label.setFixedSize(30,20)
        self.from_box = QComboBox() 
        self.from_box.setEditable(False)
        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.from_box)

        _label = QLabel('  To: ', self)
        _label.setFixedSize(20,20)
        self.to_box = QComboBox() 
        self.to_box.setEditable(False)

        controls_panel.addWidget(_label)
        controls_panel.addWidget(self.to_box)


      
        self.maptype_box = QComboBox()
        self.maptype_box.addItems(self.webView.maptypes)
        self.maptype_box.currentIndexChanged.connect(self.webView.setMap)
        controls_panel.addWidget(self.maptype_box)
           
        self.startingpoint = True
                   
        self.show()
            

    
    def mouseClick(self, lat, lng):
        self.webView.addMaker(lat, lng)
       

class myWebView (QWebEngineView):
    coordinates_form_stop = [] 
    coordinates_to_stop = [] 
    def __init__(self):
        super().__init__()

        self.maptypes = ["OpenStreetMap", "Stamen Terrain", "stamentoner", "cartodbpositron"]
        self.setMap(0)


    def add_customjs(self, map_object):
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    console.log(data)}}); """
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        html.script._children[e.get_name()] = e

        return map_object


    def handleClick(self, lat, lng):
        self.addPoint(lat, lng)


    def addSegment(self, lat1, lng1, lat2, lng2):
        js = Template(
        """
        L.polyline(
            [ [{{latitude1}}, {{longitude1}}], [{{latitude2}}, {{longitude2}}] ], {
                "color": "red",
                "opacity": 1.0,
                "weight": 4,
                "line_cap": "butt"
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude1=lat1, longitude1=lng1, latitude2=lat2, longitude2=lng2 )

        self.page().runJavaScript(js)


    def addMarker(self, lat, lng):
        js = Template(
        """
        L.marker([{{latitude}}, {{longitude}}] ).addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 7
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def addPoint(self, lat, lng):
        js = Template(
        """
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": 'green',
                "popup": "hello",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": 'green',
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.mymap.get_name(), latitude=lat, longitude=lng)
        self.page().runJavaScript(js)


    def setMap (self, i):
        self.mymap = folium.Map(location=[48.8619, 2.3519], tiles=self.maptypes[i], zoom_start=12, prefer_canvas=True)

        self.mymap = self.add_customjs(self.mymap)

        page = WebEnginePage(self)
        self.setPage(page)

        data = io.BytesIO()
        self.mymap.save(data, close_file=False)

        self.setHtml(data.getvalue().decode())

    def clearMap(self, index):
        self.setMap(index)




class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        lat_from = self.parent.coordinates_form_stop[0]
        lng_from = self.parent.coordinates_form_stop[1]
        lat_to = self.parent.coordinates_to_stop[0]
        lng_to = self.parent.coordinates_to_stop[1]

        self.parent.handleClick(lat_from, lng_from)
        self.parent.handleClick(lat_to, lng_to)
        
        self.parent.addSegment(lat_from, lat_to, lng_from, lng_to)


       
			
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
