#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*- encoding: utf-8 -*-
# Created: 02/02/2010 by defo

from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox, QAction, QIcon
from PyQt4.QtCore import QString, SIGNAL, Qt
from prymatex.gui.editor import PMXCodeEdit

from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import *
import itertools

class PMXTabWidget(QTabWidget):
    EDIT_TAB_WIDGET = PMXCodeEdit
    UNTITLED_LABEL = _("New File %s")
    
    #Signal
    currentEditorChange = pyqtSignal(PMXCodeEdit)

    counter = 1
    
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        self.setupUi()
        if not self.count():
            self.appendEmptyTab()
        
        
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeTab)
        self.connect(self, SIGNAL("currentChanged(int)"), self.indexChanged)
        self.currentChanged.connect(self.on_current_changed)
        
        self.buttonTabList = QPushButton(self)
        self.buttonTabList.setObjectName("buttonTabList")
        self.buttonTabList.setToolTip(_("Tab list"))
        self.buttonTabList.setShortcut(text_to_KeySequence("Ctrl+Tab"))
        self.buttonTabList.setIcon(QIcon(":/actions/resources/actions/view-close.png"))
        self.buttonTabList.setStyleSheet('''
            QPushButton {
                padding: 5px;
            }
        ''')
        self.setCornerWidget(self.buttonTabList, Qt.TopRightCorner)
    
    def setupUi(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        
    def untitled_label(self):
        counter = self.counter
        self.counter += 1
        return self.UNTITLED_LABEL % counter
    
    def on_current_changed(self, index):
        self.currentEditorChange.emit(self.widget(index))
        
    def mouseDoubleClickEvent(self, event):
        self.appendEmptyTab()
    
    def getEditor(self, *largs, **kwargs):
        '''
        Editor Factory
        '''
        editor =  self.EDIT_TAB_WIDGET(self, *largs, **kwargs)
        
        # TODO: Poner esto en configuración
        font = QFont()
        font.setFamily('Consolas')
        font.setPointSize(11)
        editor.setFont(font)
        return editor
    
    def on_syntax_change(self, syntax):
        editor = self.currentWidget()
        editor.set_syntax(syntax)
        
    def openLocalFile(self, path):
        '''
        Abre un archivo en una tab
        '''
        try:
            count = self.count()
            # Primero hay que buscar si no está abierto
            if count:
                for i in range(self.count()):
                    editor = self.widget(i)
                    if path == editor.path:
                        self.setCurrentWidget(editor)
                        return tabWidgetEditors
            
            if count == 1 and not self.widget(0).document().isModified() and \
                not self.widget(0).path:
                #print "Reutilizando vacio"
                editor = self.widget(0)
                
                editor.path = path
                editor.afterInsertionEvent()
                editor.getFocus()
                
            else:
                editor = self.getEditor(path)
                index = self.addTab(editor, _("Loading..."))
                self.setCurrentIndex(index)
        except UnicodeDecodeError, e:
            QMessageBox.critical(self, _("Could not decode file %s", path), 
                                 _("""<p>File %s could not be decoded</p>
                                 <p>Some exception data:</p>
                                 <pre>%s</pre>""", path, unicode(e)[:40]))
    
    def appendEmptyTab(self):
        '''
        Creates a new empty tab and returns it
        '''
        editor = self.getEditor()
        # Title should be filled after tab insertion
        index = self.addTab(editor, editor.title)
        
        self.setCurrentIndex(index)
        if self.count() == 1:
            editor.setFocus(Qt.TabFocusReason)
        return editor
    
    
    def closeTab(self, index):
        '''
        Asks the editor to be closed
        '''
        editor = self.widget(index)
        count = self.count() 
        if count == 1 and not editor.path and not editor.document().isModified():
            return
        elif count == 0:
            return
        if editor.requestClose():
            self.removeTab(index)
            return True
        return False
    
    def removeTab(self, index):
        '''
        Lets the widget know when it has been removed
        '''
        widget = self.widget(index)
        retval = QTabWidget.removeTab(self, index)
        if hasattr(widget, 'afterRemoveEvent' ):
            widget.afterRemoveEvent()
        return retval
    
    def tabRemoved(self, index):
        if not self.count():
            self.appendEmptyTab()
        # 
        widget = self.currentWidget()
        if not widget.actionMenuTab.isChecked():
            widget.actionMenuTab.setChecked(True)
            
    def indexChanged(self, index):
        #if index >= 0:
        #    widget = self.widget(index)
        #    widget.actionMenuTab.setChecked(True)
        pass
    
    def tabInserted(self, index):
        '''
        Lets the widget know when it has been inserted
        '''
        widget = self.widget(index)
        if hasattr(widget, 'afterInsertionEvent' ):
            widget.afterInsertionEvent()
        if not self.count():
            widget.actionMenuTab.setChecked(True)

class PMWTabsMenu(QMenu):
    '''
    A menu that keeps only one action active
    '''
    def __init__(self, caption, parent):
        QMenu.__init__(self, caption, parent)
        self.actionGroup = QActionGroup(self)
        self.shortcuts = []
        for i in range(1, 10):
            self.shortcuts.append(text_to_KeySequence("Alt+%d" % i))
    
    def addAction(self, action):
        QMenu.addAction(self, action)
        self.actionGroup.addAction(action)
        self.updateShortcuts()
        
    def removeAction(self, action):
        QMenu.removeAction(self, action)
        self.actionGroup.removeAction(action)
        self.updateShortcuts()
        
    def updateShortcuts(self):
        for action, shortcut in itertools.izip(self.actions(), self.shortcuts):
            action.setShortcut(shortcut)
        
    


    
        
        
        
