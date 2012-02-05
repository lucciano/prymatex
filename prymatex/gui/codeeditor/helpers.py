#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from prymatex.core.plugin import PMXBaseKeyHelper
from prymatex.support import PMXPreferenceSettings

class KeyEquivalentHelper(PMXBaseKeyHelper):
    def accept(self, editor, event, cursor = None, scope = None):
        keyseq = int(event.modifiers()) + event.key()
        self.items = self.application.supportManager.getKeyEquivalentItem(keyseq, scope)
        return bool(self.items)

    def execute(self, editor, event, cursor = None, scope = None):
        if len(self.items) == 1:
            editor.insertBundleItem(self.items[0])
        else:
            editor.selectBundleItem(self.items)

class TabTriggerHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def accept(self, editor, event, cursor = None, scope = None):
        trigger = self.application.supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.columnNumber())
        self.items = self.application.supportManager.getTabTriggerItem(trigger, scope) if trigger is not None else []
        return bool(self.items)

    def execute(self, editor, event, cursor = None, scope = None):
        #Inserto los items
        if len(self.items) == 1:
            editor.insertBundleItem(self.items[0], tabTriggered = True)
        else:
            editor.selectBundleItem(self.items, tabTriggered = True)

class CompleterHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Space
    def accept(self, editor, event, cursor = None, scope = None):
        """accept the completer event"""
        if event.modifiers() == QtCore.Qt.ControlModifier:
            settings = self.application.supportManager.getPreferenceSettings(scope)
            #an array of additional candidates when cycling through completion candidates from the current document.
            self.completions = settings.completions
            #a shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
            self.completionCommand = settings.completionCommand
            self.disableDefaultCompletion = settings.disableDefaultCompletion
            print self.completions, self.completionCommand, self.disableDefaultCompletion
            return bool(self.completions)
        return False
            
    def execute(self, editor, event, cursor = None, scope = None):
        currentWord, start, end = editor.getCurrentWord()
        #alreadyTyped
        editor.showCompleter(self.completions, currentWord)

class SmartTypingPairsHelper(PMXBaseKeyHelper):
    def accept(self, editor, event, cursor = None, scope = None):
        settings = self.application.supportManager.getPreferenceSettings(scope)
        character = event.text()
        pairs = filter(lambda pair: character == pair[0], settings.smartTypingPairs)
        self.pair = pairs[0] if len(pairs) == 1 else []
        
        #Si no tengo nada termino
        if not bool(self.pair): return False

        #Vamos a intentar algo radical
        openTyping = map(lambda pair: pair[0], settings.smartTypingPairs)
        closeTyping = map(lambda pair: pair[1], settings.smartTypingPairs)
        self.cursorOpen = self.cursorClose = None
        if cursor.hasSelection():
            character = cursor.selectedText()
            if character in openTyping:
                #Es un caracter especial de apertura
                self.cursorOpen = cursor
                index = openTyping.index(character)
                self.cursorClose = editor.findTypingPair(character, closeTyping[index], cursor)
            elif character in closeTyping:
                #Es un caracter especial de cierre
                self.cursorClose = cursor
                index = closeTyping.index(character)
                self.cursorOpen = editor.findTypingPair(character, openTyping[index], cursor, True)
            return True
        elif character in openTyping:
            leftChar = cursor.document().characterAt(cursor.position() - 1)
            rightChar = cursor.document().characterAt(cursor.position())
            #Buscar de izquierda a derecha por dentro
            pairs = filter(lambda pair: leftChar == pair[0] and rightChar != pair[1], editor.braces)
            if pairs:
                pair = pairs[0]
                self.cursorOpen = cursor
                cursor = QtGui.QTextCursor(self.cursorOpen)
                cursor.setPosition(cursor.position() - 1)
                self.cursorClose = editor.findTypingPair(pair[0], pair[1], cursor)
                self.cursorClose.setPosition(self.cursorClose.selectionStart())
                return bool(self.pair)
            #Buscar de izquierda a derecha por fuera
            pairs = filter(lambda pair: rightChar == pair[0], editor.braces)
            if pairs:
                pair = pairs[0]
                self.cursorOpen = cursor
                self.cursorClose = editor.findTypingPair(pair[0], pair[1], self.cursorOpen)
                self.cursorClose.setPosition(self.cursorClose.selectionEnd())
                return bool(self.pair)
        elif character in closeTyping and character not in openTyping:
            rightChar = cursor.document().characterAt(cursor.position())
            leftChar = cursor.document().characterAt(cursor.position() - 1)
            #Buscar de derecha a izquierda por dentro
            pairs = filter(lambda pair: rightChar == pair[1] and leftChar != pair[0], editor.braces)
            if pairs:
                pair = pairs[0]
                self.cursorClose = cursor
                cursor = QtGui.QTextCursor(self.cursorClose)
                cursor.setPosition(cursor.position() + 1)
                self.cursorOpen = editor.findTypingPair(pair[1], pair[0], cursor, True)
                self.cursorOpen.setPosition(self.cursorOpen.selectionEnd())
                return bool(self.pair)
            #Buscar de derecha a izquierda por fuera
            pairs = filter(lambda pair: leftChar == pair[1], editor.braces)
            if pairs:
                pair = pairs[0]
                self.cursorClose = cursor
                self.cursorOpen = editor.findTypingPair(pair[1], pair[0], cursor, True)
                self.cursorOpen.setPosition(self.cursorOpen.selectionStart())
                return bool(self.pair)
        return bool(self.pair)

    def execute(self, editor, event, cursor = None, scope = None):
        cursor = editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            if self.cursorClose is not None and self.cursorOpen is not None:
                self.cursorOpen.insertText(self.pair[0])
                self.cursorClose.insertText(self.pair[1])
            else:
                position = cursor.selectionStart()
                text = self.pair[0] + cursor.selectedText() + self.pair[1]
                cursor.insertText(text)
                cursor.setPosition(position)
                cursor.setPosition(position + len(text), QtGui.QTextCursor.KeepAnchor)
                editor.setTextCursor(cursor)
        elif self.cursorOpen is None:
            position = cursor.position()
            cursor.insertText("%s%s" % (self.pair[0], self.pair[1]))
            cursor.setPosition(position + 1)
            editor.setTextCursor(cursor)
        else:
            self.cursorOpen.insertText(self.pair[0])
            self.cursorClose.insertText(self.pair[1])
        cursor.endEditBlock()

class MoveCursorToHomeHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Home
    def accept(self, editor, event, cursor = None, scope = None):
        #Solo si el cursor no esta al final de la indentacion
        block = cursor.block()
        self.newPosition = block.position() + len(block.userData().indent)
        return self.newPosition != cursor.position()
        
    def execute(self, editor, event, cursor = None, scope = None):
        #Lo muevo al final de la indentacion
        cursor = editor.textCursor()
        cursor.setPosition(self.newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
        editor.setTextCursor(cursor)

class OverwriteHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Insert
    def execute(self, editor, event, cursor = None, scope = None):
        editor.setOverwriteMode(not editor.overwriteMode())
        editor.modeChanged.emit()
        
class TabIndentHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Tab
    def execute(self, editor, event, cursor = None, scope = None):
        start, end = editor.getSelectionBlockStartEnd()
        if start != end:
            editor.indentBlocks()
        elif editor.getSyntax().indentSensitive:
            #Smart indent
            cursor = editor.textCursor()
            position = cursor.position()
            blockPosition = cursor.block().position()
            indent = cursor.block().userData().indent
            editor.textCursor().insertText(editor.tabKeyBehavior)
        else:
            editor.textCursor().insertText(editor.tabKeyBehavior)

class BackspaceUnindentHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Backspace
    def accept(self, editor, event, cursor = None, scope = None):
        if cursor.hasSelection(): return False
        indent = len(cursor.block().userData().indent)
        return indent != 0 and indent == cursor.columnNumber()
        
    def execute(self, editor, event, cursor = None, scope = None):
        cursor = editor.textCursor()
        for _ in range(len(editor.tabKeyBehavior)):
            cursor.deletePreviousChar()

class BacktabUnindentHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Backtab
    def execute(self, editor, event, cursor = None, scope = None):
        start, end = editor.getSelectionBlockStartEnd()
        if start != end:
            editor.unindentBlocks()
        else:
            cursor = editor.textCursor()
            block = cursor.block()
            userData = cursor.block().userData()
            counter = editor.tabStopSize if len(userData.indent) > editor.tabStopSize else len(userData.indent)
            for _ in range(counter):
                cursor.deletePreviousChar()

class SmartUnindentHelper(PMXBaseKeyHelper):
    def accept(self, editor, event, cursor = None, scope = None):
        if event.text():
            settings = self.application.supportManager.getPreferenceSettings(scope)
            block = cursor.block()
            text = block.text()[:cursor.columnNumber()] + event.text()
            indentMarks = settings.indent(text)
            if PMXPreferenceSettings.INDENT_DECREASE in indentMarks:
                previous = block.previous()
                return previous.isValid() and block.userData().indent >= previous.userData().indent
        return False
        
    def execute(self, editor, event, cursor = None, scope = None):
        QtGui.QPlainTextEdit.keyPressEvent(editor, event)
        cursor = editor.textCursor()
        cursor.setPosition(cursor.block().position())
        for _ in range(len(editor.tabKeyBehavior)):
            cursor.deleteChar()

class SmartIndentHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_Return
    def accept(self, editor, event, cursor = None, scope = None):
        self.settings = self.application.supportManager.getPreferenceSettings(scope)
        return True
        
    def execute(self, editor, event, cursor = None, scope = None):
        cursor = editor.textCursor()
        block = cursor.block()
        text = block.text()[:cursor.columnNumber()]
        if editor.document().blockCount() == 1:
            syntax = self.application.supportManager.findSyntaxByFirstLine(text)
            if syntax is not None:
                editor.setSyntax(syntax)
        indentMarks = self.settings.indent(text)
        if PMXPreferenceSettings.INDENT_INCREASE in indentMarks:
            self.logger.debug("Increase indent")
            indent = block.userData().indent + editor.tabKeyBehavior
        elif PMXPreferenceSettings.INDENT_NEXTLINE in indentMarks:
            self.logger.debug("Increase next line indent")
        elif PMXPreferenceSettings.UNINDENT in indentMarks:
            self.logger.debug("Unindent")
            indent = ""
        elif PMXPreferenceSettings.INDENT_DECREASE in indentMarks:
            indent = block.userData().indent[:len(editor.tabKeyBehavior)]
        else:
            self.logger.debug("Preserve indent")
            indent = block.userData().indent
        cursor.insertText("\n%s" % indent)

class MultiCursorHelper(PMXBaseKeyHelper):
    KEY = QtCore.Qt.Key_M
    def accept(self, editor, event, cursor = None, scope = None):
        return event.key() == self.KEY and event.modifiers() & QtCore.Qt.ControlModifier and event.modifiers() & QtCore.Qt.MetaModifier

    def execute(self, editor, event, cursor = None, scope = None):
        cursor = cursor or editor.textCursor()
        if not cursor.hasSelection():
            text, start, end = editor.getCurrentWord()
            newCursor = QtGui.QTextCursor(cursor)
            newCursor.setPosition(start)
            newCursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            editor.multiCursorMode.addMergeCursor(newCursor)
        else:
            text = cursor.selectedText()
            editor.multiCursorMode.addMergeCursor(cursor)
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                newCursor = editor.document().find(text, cursor, QtGui.QTextDocument.FindBackward)
            else:
                newCursor = editor.document().find(text, cursor)
            if not newCursor.isNull():
                editor.multiCursorMode.addMergeCursor(newCursor)