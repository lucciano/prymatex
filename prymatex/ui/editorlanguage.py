# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/editorlanguage.ui'
#
# Created: Thu Jul 14 20:29:23 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Language(object):
    def setupUi(self, Language):
        Language.setObjectName(_fromUtf8("Language"))
        Language.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(Language)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.content = QtGui.QPlainTextEdit(Language)
        self.content.setObjectName(_fromUtf8("content"))
        self.verticalLayout.addWidget(self.content)

        self.retranslateUi(Language)
        QtCore.QMetaObject.connectSlotsByName(Language)

    def retranslateUi(self, Language):
        Language.setWindowTitle(_('Form'))

