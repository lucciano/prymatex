# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/support/templatefile.ui'
#
# Created: Fri Nov  9 18:10:45 2012
#      by: PyQt4 UI code generator snapshot-4.9.6-95094339d25b
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TemplateFile(object):
    def setupUi(self, TemplateFile):
        TemplateFile.setObjectName(_fromUtf8("TemplateFile"))
        TemplateFile.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(TemplateFile)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.content = QtGui.QPlainTextEdit(TemplateFile)
        self.content.setObjectName(_fromUtf8("content"))
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(TemplateFile)
        QtCore.QMetaObject.connectSlotsByName(TemplateFile)

    def retranslateUi(self, TemplateFile):
        TemplateFile.setWindowTitle(_('Form'))

