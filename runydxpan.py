# -*- coding: utf-8 -*-
import os
from PyQt5.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon, QCursor, QPixmap
from qgis.core import QgsProject, QgsRasterLayer
from .getydxpan import GetYdxPan

class YdxPanRun:   
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = (QAction(QIcon(os.path.dirname(__file__) + "/icon.svg"),
            'Yandex Panoramas',
            self.iface.mainWindow()))
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Yandex Panoramas", self.action)

    def unload(self):
        self.iface.removePluginMenu('&Yandex Panoramas', self.action)
        self.iface.removeToolBarIcon(self.action)
        del self.action
        
    def run(self):
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name()=='Yandex Panoramas':
                QgsProject.instance().removeMapLayers( [layer.id()] )
        
        self.layer_path = QgsRasterLayer('http-header:referer=&type=xyz&url=https://vec02.core-stv-renderer.maps.yandex.net/2.x/tiles?l%3Dstv%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D%26lang%3Dru_RU%26v%3D2025.03.23.22.34-1_25.03.21-1-24259%26format%3Dpng&zmax=18&zmin=0', 'Yandex Panoramas', 'wms')
        self.crs = self.layer_path.crs()
        self.crs.createFromId(3395)
        self.layer_path.setCrs(self.crs)
        QgsProject.instance().addMapLayer(self.layer_path)

        canvas = self.iface.mapCanvas()
        self.tool = GetYdxPan(canvas)
        canvas.setMapTool(self.tool)

        pixmap = QPixmap(os.path.dirname(__file__) + "/cursor.svg")
        cursor = QCursor(pixmap, hotX=10, hotY=10)
        canvas.setCursor(cursor)
