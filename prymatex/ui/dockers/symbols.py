# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dockers/symbols.ui'
#
# Created: Fri Nov  9 18:10:46 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SymbolsDock(object):
    def setupUi(self, SymbolsDock):
        SymbolsDock.setObjectName(_fromUtf8("SymbolsDock"))
        SymbolsDock.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeViewSymbols = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewSymbols.setObjectName(_fromUtf8("treeViewSymbols"))
        self.verticalLayout.addWidget(self.treeViewSymbols)
        SymbolsDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(SymbolsDock)
        QtCore.QMetaObject.connectSlotsByName(SymbolsDock)

    def retranslateUi(self, SymbolsDock):
        SymbolsDock.setWindowTitle(_('Symbols'))

