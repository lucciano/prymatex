#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBaseWidgetPlugin

class PMXBaseStatusBar(PMXBaseWidgetPlugin):
    def setCurrentEditor(self, editor):
        pass
    
    def setMainWindow(self, mainWindow):
        self.mainWindow = mainWindow