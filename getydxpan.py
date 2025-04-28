# -*- coding: utf-8 -*-
from qgis.utils import iface
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.core import QgsPointXY, QgsWkbTypes, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from math import atan2, degrees, log
import webbrowser

class GetYdxPan(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.iface = iface
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        
        self.rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.setColor(QColor(255, 0, 0, 100))
        self.rubber_band.setWidth(3)
        
        self.start_marker = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.PointGeometry)
        self.start_marker.setColor(QColor(255, 0, 0, 250))
        self.start_marker.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.start_marker.setIconSize(10)

        self.end_marker = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.PointGeometry)
        self.end_marker.setColor(QColor(0, 255, 255, 250))
        self.end_marker.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.end_marker.setIconSize(5)
                
        self.reset()

    def reset(self):
        self.start_point = None
        self.end_point = None
        self.rubber_band.reset(QgsWkbTypes.LineGeometry)
        self.start_marker.reset(QgsWkbTypes.PointGeometry)
        self.end_marker.reset(QgsWkbTypes.PointGeometry)

    def canvasPressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.start_point is None:
                self.start_point = self.toMapCoordinates(event.pos())
                self.start_marker.addPoint(self.start_point)
                self.start_marker.show()
                self.rubber_band.addPoint(self.start_point)
            elif self.end_point is None:
                self.end_point = self.toMapCoordinates(event.pos())
                self. end_marker.addPoint(self.end_point)
                self.end_marker.show()
                self.rubber_band.addPoint(self.end_point)
                                
                point = self.start_point
                
                crs = self.canvas.mapSettings().destinationCrs()
                crs_dest = QgsCoordinateReferenceSystem("EPSG:4326")
                transform = QgsCoordinateTransform(crs, crs_dest, QgsProject.instance())
                        
                point_transformed = transform.transform(point)
                current_scale = self.canvas.scale()

                dx = self.end_point.x() - self.start_point.x()
                dy = self.end_point.y() - self.start_point.y()
                azimuth = (degrees(atan2(dx, dy))) % 360
                    
                zoom_level = round(log(591657550.5 / current_scale, 2))
                    
                link = f'https://yandex.ru/maps/?indoorLevel=1&ll={point_transformed.x()}%2C{point_transformed.y()}&panorama%5Bdirection%5D={azimuth}%2C0.000000&panorama%5Bfull%5D=true&panorama%5Bpoint%5D={point_transformed.x()}%2C{point_transformed.y()}&panorama%5Bspan%5D=127.617127%2C60.000000&z={zoom_level}'
                webbrowser.open(link, new=0)
            
            elif self.start_point:
                self.reset()
                self.start_point = self.toMapCoordinates(event.pos())
                self.start_marker.addPoint(self.start_point)
                self.start_marker.show()
                self.rubber_band.addPoint(self.start_point)
                             
        elif event.button() == Qt.RightButton:
            self.reset()

    def canvasMoveEvent(self, event):
        if self.start_point is not None and self.end_point is None:
            current_point = self.toMapCoordinates(event.pos())
            self.rubber_band.reset(QgsWkbTypes.LineGeometry)
            self.rubber_band.addPoint(self.start_point)
            self.rubber_band.addPoint(current_point)

    def deactivate(self):
        self.reset()
        super().deactivate()
