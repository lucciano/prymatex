'''
Search and replace module
'''
from PyQt4 import QtCore
from PyQt4.Qt import QComboBox, QTextCursor,QTextDocument
from PyQt4.Qt import Qt, QRegExp
from internalwidgets import PMXRefocusWidget

class PMXFindReplaceWidget(PMXRefocusWidget):
    '''
    Holds the find/replace logic
    Works with editorwidget.ui findReplaceWidget widgets (find next, find previous).
    '''
    findMatchCountChanged = QtCore.pyqtSignal(int)
    searchFlagsChanged = QtCore.pyqtSignal()
    focusFindBox = QtCore.pyqtSignal()
    
    def findFirstTime(self, text):
        '''
        Same as find next but it updates match counter
        through signal.
        '''
        self.regexp = text # Property
            
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.textEdit.setTextCursor(cursor)
        
        found_cursors = []
        
        while True:
            
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)

            if cursor.isNull():
                break
            found_cursors.append(cursor)
            
        if found_cursors:
            self.textEdit.setTextCursor(found_cursors[0])
            
        self.findMatchCountChanged.emit( len(found_cursors) )
        #print "findMatchCountChanged.emit(",  len(found_cursors), ")"
        
    def findNext(self):
        cursor = self.textEdit.document().find(self.regexp, self.textEdit.textCursor(), self.flags)
        if cursor.isNull():
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.textEdit.setTextCursor(cursor)
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)
        if not cursor.isNull():
            self.textEdit.setTextCursor(cursor)
    
    def findPrevious(self):
        cursor = self.textEdit.document().find(self.regexp, self.textEdit.textCursor(), self.flags | QTextDocument.FindBackward)
        if cursor.isNull():
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags | QTextDocument.FindBackward)
        if not cursor.isNull():
            self.textEdit.setTextCursor(cursor)
    
    # Property for the text edit
    __textEdit = None
    def setTextEdit(self, textedit):
        self.__textEdit = textedit
    textEdit = property(fget = lambda s: s.__textEdit, fset = setTextEdit)
    
    
    __caseSensitive = False
    def setCaseSensitive(self, toggled):
        self.__caseSensitive = toggled
        self.searchFlagsChanged.emit()
    
    caseSensitive = property(fget = lambda s: s.__caseSensitive, fset = setCaseSensitive,
                             doc = 'Flag for find case sensitivity in find menu options')
    
    __useRegex = False
    def setUseRegex(self, toggled):
        self.__useRegex = toggled
        print "Use regex", toggled
        self.searchFlagsChanged.emit()
    
    useRegex = property(fget = lambda s: s.__useRegex, fset = setUseRegex,
                        doc = ''' Falg for Use regular expression in find menu options''')
    
    __wholeWord = False
    def setWholeWord(self, toggled):
        self.__wholeWord = toggled
        self.searchFlagsChanged.emit()
        
    wholeWord = property(fget = lambda s: s.__wholeWord, fset = setWholeWord, 
                         doc = 'Flag for find Whole Word in find menu options')
    
    __regexp = None
    @property
    def regexp(self):
        '''
        Current search text wrapped in a QRegExp instance
        '''
        return self.__regexp
    
    def _isSafeRegex(self, text):
        # TODO: Move this logic to the combo box
        if text in ('^', '^$', '$'):
            return False
        return True
    
    @regexp.setter
    def regexp(self, text):
        if isinstance(text, (basestring, str)):
            if self.useRegex:
                regex = QtCore.QRegExp(text)
                if regex.isValid() and self._isSafeRegex(text):
                    self.__regexp = regex # Avoids infinite loop   
            else:
                self.__regexp = QRegExp(QRegExp.escape(text))
                
            if self.caseSensitive:
                caseSensitivity = Qt.CaseSensitive
            else:
                caseSensitivity = Qt.CaseInsensitive
            self.__regexp.setCaseSensitivity(caseSensitivity)    
        else:
            raise ValueError("Can't set regrexp from %s (%s)" % (text, type(text)))
    
    @property
    def flags(self):
        '''
        Flags property for QTextDocument.find(..., flags)
        '''
        flags = QTextDocument.FindFlags(0)
        
        if self.wholeWord:
            flags |= QTextDocument.FindWholeWords
        return flags
    
    __replacement = None
    @property
    def setReplacement(self, text):
        self.__replacement = text
    replacement = property(fget = lambda s: s.__replacement, fset = setReplacement)
    
    def replace(self, text):
        print "replace with", self.regexp, text
        if not self.regexp:
            # Tehre's no pattern to find, let's focus find box
            self.focusFindBox.emit()
            return
        
        self.replacement = text
        # Start from begining?
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.textEdit.setTextCursor(cursor)
        
        cursor = self.textEdit.textCursor()
        cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)
        if not cursor.isNull():
            cursor.beginEditBlock()
            #cursor.clearSelection()
            #cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
            cursor.insertText(self.replacement)
            #cur
            cursor.endEditBlock()
        
        return cursor
    
    def replaceAndFindNext(self):
        cursor = self.textEdit.textCursor()
        cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)
        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(self.replacement)
            cursor.endEditBlock()
            cursor = self.textEdit.document().find(self.regexp, cursor, self.flags)
            if not cursor.isNull():
                self.textEdit.setTextCursor(cursor)
    
    def replaceAndFindPrevious(self):
        pass
    
    
        
class PMXFindBox(QComboBox):
    
    # Some constants
    
    KEY_TRIGGERS = (Qt.Key_Escape, )
    STYLE_NO_MATCH = ''' background-color: red; color: #fff; '''
    STYLE_MATCH = ' background-color: #dea;'
    STYLE_NORMAL = ''
    
    # Signals
    editionFinished = QtCore.pyqtSignal()
    findRequested = QtCore.pyqtSignal(str)
    findNextRequested  = QtCore.pyqtSignal()
    
    def __init__(self, parent = None):
        super(PMXFindBox, self).__init__(parent)
        self.editTextChanged.connect(self.textChanged)
    
    def keyPressEvent(self, event):
        super(PMXFindBox, self).keyPressEvent(event)
        key = event.key() 
        if key in self.KEY_TRIGGERS:
            self.editionFinished.emit()
            
        elif key in (Qt.Key_Backspace, Qt.Key_Delete):
            if self.currentText().length():
                self.findRequested.emit(self.currentText())
            
        elif key in (Qt.Key_Return, ):
            self.findNextRequested.emit()
    
    def showEvent(self, event):
        super(PMXFindBox, self).showEvent(event)
        self.setStyleSheet(self.STYLE_NORMAL)
    
    def optionsChanged(self):
        '''
        Called when flags changed, if there's text available
        re-emits findFirstTime signal
        '''
        if self.currentText():
            self.findRequested.emit(self.currentText())
    
    def findMatchCountChanged(self, count):
        #print "Find count changed"
        if count == 0:
            self.setStyleSheet(self.STYLE_NO_MATCH)
        else:
            self.setStyleSheet(self.STYLE_MATCH)
    
    def textChanged(self, text):
        
        if text.length() == 0:
            self.setStyleSheet(self.STYLE_NORMAL)
        else:
            #print "Find requested"
            self.findRequested.emit(text)
        
    
    

class PMXReplaceBox(QComboBox):
    '''
    Editable QComboBox where the user types the replace text
    '''
    editionFinished = QtCore.pyqtSignal()
    replaceTextRequested = QtCore.pyqtSignal(str)
    
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def keyPressEvent(self, event):
        super(PMXReplaceBox, self).keyPressEvent(event)
        key = event.key()
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()
        elif key in (Qt.Key_Return, Qt.Key_Backspace, Qt.Key_Delete):
            current_text = self.currentText()
            if current_text.length():
                self.replaceTextRequested.emit(current_text)
    
    

class PMXCommonSearchBox(QComboBox):
    '''
    Common behaviour between the search and replace widgtets
    '''
    editionFinished = QtCore.pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def keyPressEvent(self, event):
        super(PMXCommonSearchBox, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()