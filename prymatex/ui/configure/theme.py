# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/theme.ui'
#
# Created: Wed Jan 23 09:31:01 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FontTheme(object):
    def setupUi(self, FontTheme):
        FontTheme.setObjectName(_fromUtf8("FontTheme"))
        FontTheme.resize(605, 728)
        self.verticalLayout_2 = QtGui.QVBoxLayout(FontTheme)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBoxFont_2 = QtGui.QGroupBox(FontTheme)
        self.groupBoxFont_2.setObjectName(_fromUtf8("groupBoxFont_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBoxFont_2)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setMargin(6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.fontComboBoxName = QtGui.QFontComboBox(self.groupBoxFont_2)
        self.fontComboBoxName.setFontFilters(QtGui.QFontComboBox.MonospacedFonts)
        self.fontComboBoxName.setObjectName(_fromUtf8("fontComboBoxName"))
        self.horizontalLayout_4.addWidget(self.fontComboBoxName)
        self.spinBoxFontSize = QtGui.QSpinBox(self.groupBoxFont_2)
        self.spinBoxFontSize.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxFontSize.setMinimum(7)
        self.spinBoxFontSize.setObjectName(_fromUtf8("spinBoxFontSize"))
        self.horizontalLayout_4.addWidget(self.spinBoxFontSize)
        self.checkBoxAntialias = QtGui.QCheckBox(self.groupBoxFont_2)
        self.checkBoxAntialias.setMaximumSize(QtCore.QSize(80, 16777215))
        self.checkBoxAntialias.setObjectName(_fromUtf8("checkBoxAntialias"))
        self.horizontalLayout_4.addWidget(self.checkBoxAntialias)
        self.verticalLayout_2.addWidget(self.groupBoxFont_2)
        self.groupBoxTheme = QtGui.QGroupBox(FontTheme)
        self.groupBoxTheme.setObjectName(_fromUtf8("groupBoxTheme"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBoxTheme)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBoxThemes = QtGui.QComboBox(self.groupBoxTheme)
        self.comboBoxThemes.setObjectName(_fromUtf8("comboBoxThemes"))
        self.verticalLayout.addWidget(self.comboBoxThemes)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonInvisibles = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonInvisibles.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonInvisibles.setText(_fromUtf8(""))
        self.pushButtonInvisibles.setObjectName(_fromUtf8("pushButtonInvisibles"))
        self.gridLayout.addWidget(self.pushButtonInvisibles, 0, 3, 1, 1)
        self.pushButtonSelection = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonSelection.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonSelection.setText(_fromUtf8(""))
        self.pushButtonSelection.setObjectName(_fromUtf8("pushButtonSelection"))
        self.gridLayout.addWidget(self.pushButtonSelection, 2, 1, 1, 1)
        self.pushButtonCaret = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonCaret.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonCaret.setText(_fromUtf8(""))
        self.pushButtonCaret.setObjectName(_fromUtf8("pushButtonCaret"))
        self.gridLayout.addWidget(self.pushButtonCaret, 2, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBoxTheme)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBoxTheme)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBoxTheme)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 3, 2, 1, 1)
        self.pushButtonBackground = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonBackground.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonBackground.setText(_fromUtf8(""))
        self.pushButtonBackground.setObjectName(_fromUtf8("pushButtonBackground"))
        self.gridLayout.addWidget(self.pushButtonBackground, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBoxTheme)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBoxTheme)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.pushButtonForeground = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonForeground.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonForeground.setText(_fromUtf8(""))
        self.pushButtonForeground.setObjectName(_fromUtf8("pushButtonForeground"))
        self.gridLayout.addWidget(self.pushButtonForeground, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBoxTheme)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.pushButtonGutterBackground = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonGutterBackground.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonGutterBackground.setText(_fromUtf8(""))
        self.pushButtonGutterBackground.setObjectName(_fromUtf8("pushButtonGutterBackground"))
        self.gridLayout.addWidget(self.pushButtonGutterBackground, 3, 3, 1, 1)
        self.pushButtonLineHighlight = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonLineHighlight.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonLineHighlight.setText(_fromUtf8(""))
        self.pushButtonLineHighlight.setObjectName(_fromUtf8("pushButtonLineHighlight"))
        self.gridLayout.addWidget(self.pushButtonLineHighlight, 1, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBoxTheme)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBoxTheme)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.pushButtonGutterForeground = QtGui.QPushButton(self.groupBoxTheme)
        self.pushButtonGutterForeground.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonGutterForeground.setText(_fromUtf8(""))
        self.pushButtonGutterForeground.setObjectName(_fromUtf8("pushButtonGutterForeground"))
        self.gridLayout.addWidget(self.pushButtonGutterForeground, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableViewStyles = QtGui.QTableView(self.groupBoxTheme)
        self.tableViewStyles.setShowGrid(False)
        self.tableViewStyles.setSortingEnabled(True)
        self.tableViewStyles.setObjectName(_fromUtf8("tableViewStyles"))
        self.verticalLayout.addWidget(self.tableViewStyles)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonAdd = QtGui.QPushButton(self.groupBoxTheme)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout_3.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(self.groupBoxTheme)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-remove"))
        self.pushButtonRemove.setIcon(icon)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout_3.addWidget(self.pushButtonRemove)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_9 = QtGui.QLabel(self.groupBoxTheme)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.comboBoxScope = QtGui.QComboBox(self.groupBoxTheme)
        self.comboBoxScope.setEditable(True)
        self.comboBoxScope.setObjectName(_fromUtf8("comboBoxScope"))
        self.horizontalLayout_3.addWidget(self.comboBoxScope)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBoxTheme)

        self.retranslateUi(FontTheme)
        QtCore.QMetaObject.connectSlotsByName(FontTheme)

    def retranslateUi(self, FontTheme):
        FontTheme.setWindowTitle(_('Form'))
        self.groupBoxFont_2.setTitle(_('Font'))
        self.checkBoxAntialias.setText(_('Anti alias'))
        self.groupBoxTheme.setTitle(_('Theme'))
        self.label_6.setText(_('Invisibles:'))
        self.label_4.setText(_('Background:'))
        self.label_10.setText(_('Gutter background:'))
        self.label_5.setText(_('Selection:'))
        self.label_3.setText(_('Foreground:'))
        self.label_7.setText(_('Caret:'))
        self.label_8.setText(_('Line highlight:'))
        self.label_11.setText(_('Gutter foreground:'))
        self.label_9.setText(_('Scope selector:'))

