# -*- coding: utf-8 -*-
# Yandex-panoramas-qgis-plugin
# Licensed under the terms of GNU GPL 2
# Thanks to Martin Dobias for the 'QGIS Minimalist Plugin Skeleton': 
#   https://github.com/wonder-sk/qgis-minimal-plugin

from .runydxpan import YdxPanRun

def classFactory(iface):    
    return YdxPanRun(iface)
