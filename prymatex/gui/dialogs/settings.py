#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog
from prymatex.models.settings import SettingsTreeModel as PMXConfigureTreeModel
from prymatex.models.settings import SortFilterSettingsProxyModel as PMXConfigureProxyModel

class PMXSettingsDialog(QtGui.QDialog, Ui_TreeWidgetDialog):
    """Settings dialog, it's hold by the application under configdialog property
    """
    def __init__(self, application):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.application = application
        
        self.baseWindowTitle = self.windowTitle()
        
        self.model = PMXConfigureTreeModel(self)
        self.model.proxySettingsCreated.connect(self.on_model_proxySettingsCreated)
        
        self.proxyModelSettings = PMXConfigureProxyModel(self)
        self.proxyModelSettings.setSourceModel(self.model)
        
        self.treeView.setModel(self.proxyModelSettings)

        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        self.widgetsLayout.addWidget(self.stackedWidget)
    
    def on_model_proxySettingsCreated(self, proxyWidget):
        self.stackedWidget.addWidget(proxyWidget)

    def selectFirstIndex(self):
        firstIndex = self.proxyModelSettings.index(0, 0)
        rect = self.treeView.visualRect(firstIndex)
        self.treeView.setSelection(rect, QtGui.QItemSelectionModel.ClearAndSelect)
        treeNode = self.proxyModelSettings.node(firstIndex)
        self.setCurrentSettingWidget(treeNode)

    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelSettings.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
        self.selectFirstIndex()
        
    def on_treeView_pressed(self, index):
        treeNode = self.proxyModelSettings.node(index)
        self.setCurrentSettingWidget(treeNode)
        
    def on_treeView_activated(self, index):
        treeNode = self.proxyModelSettings.node(index)
        self.setCurrentSettingWidget(treeNode)
    
    def setCurrentSettingWidget(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        self.textLabelTitle.setText(widget.title())
        self.textLabelPixmap.setPixmap(widget.icon().pixmap(20, 20))
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, widget.title()))
    
    def register(self, widget):
        index = self.stackedWidget.addWidget(widget)
        self.model.addConfigNode(widget)
    
    def loadSettings(self):
        for index in xrange(self.stackedWidget.count()):
            self.stackedWidget.widget(index).loadSettings()
        self.selectFirstIndex()