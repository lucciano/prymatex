#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QColor

from prymatex import resources
from prymatex.core.plugin.editor import PMXBaseEditorAddon
from prymatex.gui.codeeditor.addons import HighlightCurrentSelectionAddon

class CodeEditorSideBar(QtGui.QWidget):
    updateRequest = QtCore.pyqtSignal()
    
    def __init__(self, editor):
        QtGui.QWidget.__init__(self, editor)
        self.editor = editor
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        
    def addWidget(self, widget):
        self.horizontalLayout.addWidget(widget)
        widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in [ QtCore.QEvent.Hide, QtCore.QEvent.Show ]:
            self.updateRequest.emit()
            return True
        return QtCore.QObject.eventFilter(self, obj, event)

    def width(self):
        width = 0
        for index in range(self.horizontalLayout.count()):
            widget = self.horizontalLayout.itemAt(index).widget()
            if widget.isVisible():
                width += widget.width()
        return width

    def scroll(self, *largs):
        for index in range(self.horizontalLayout.count()):
            self.horizontalLayout.itemAt(index).widget().scroll(*largs)

#========================================
# BASE EDITOR SIDEBAR ADDON
#========================================
class SideBarWidgetAddon(PMXBaseEditorAddon):
    ALIGNMENT = None

    def translatePosition(self, position):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        fh = font_metrics.lineSpacing()
        ys = position.y()
        
        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        page_bottom = self.editor.viewport().height()
        while block.isValid():
            blockPosition = self.editor.blockBoundingGeometry(block).topLeft() + offset
            if blockPosition.y() > page_bottom:
                break
            if blockPosition.y() < ys and (blockPosition.y() + fh) > ys:
                break
            block = block.next()
        return block

#=======================================
# SideBar Widgets
#=======================================
class LineNumberSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    MARGIN = 10
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.foreground = self.editor.colours["foreground"]
        self.normalFont = QtGui.QFont(self.editor.font)
        self.boldFont = QtGui.QFont(self.editor.font)
        self.boldFont.setBold(True)
        self.normalMetrics = QtGui.QFontMetrics(self.normalFont)
        self.boldMetrics = QtGui.QFontMetrics(self.boldFont)
        
        self.setFixedWidth(self.fontMetrics().width("0") + self.MARGIN)

        self.editor.blockCountChanged.connect(self.updateWidth)
        self.editor.themeChanged.connect(self.updateColours)
    
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.foreground = self.editor.colours["foreground"]
        self.update()

    def updateWidth(self, newBlockCount):
        width = self.fontMetrics().width(str(newBlockCount)) + self.MARGIN
        if self.width() != width:
            self.setFixedWidth(width)
            #self.updateSideBarRequest.emit()

    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowLineNumbers_toggled(editor, checked):
            instance = editor.addonByClass(cls)
            instance.setVisible(checked)

        def on_actionShowLineNumbers_testChecked(editor):
            instance = editor.addonByClass(cls)
            return instance.isVisible()
        
        baseMenu = ("View", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {'title': "Line Numbers",
            'callback': on_actionShowLineNumbers_toggled,
            'shortcut': 'F10',
            'checkable': True,
            'testChecked': on_actionShowLineNumbers_testChecked }
        return { baseMenu: menuEntry }

    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())
        
        painter = QtGui.QPainter(self)
        painter.setPen(self.foreground)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        line_count = block.blockNumber()
        
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                numberText = str(line_count)
                if block == current_block:
                    painter.setFont(self.boldFont)
                    leftPosition = self.width() - (self.boldMetrics.width(numberText) + round(self.MARGIN / 2))
                    topPosition = position.y() + self.boldMetrics.ascent() + self.boldMetrics.descent() - 2
                    painter.drawText(leftPosition, topPosition, numberText)
                else:
                    painter.setFont(self.normalFont)
                    leftPosition = self.width() - (self.normalMetrics.width(numberText) + round(self.MARGIN / 2))
                    topPosition = position.y() + self.normalMetrics.ascent() + self.normalMetrics.descent() - 2
                    painter.drawText(leftPosition, topPosition, numberText)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
    """
    __foreground = QtGui.QColor()
    @property
    def foreground(self):
        return self.__foreground
    
    @foreground.setter
    def foreground(self, color):
        assert isinstance(color, QtGui.QColor)
        # http://www.qtcentre.org/wiki/index.php?title=Adaptive_Coloring_for_Syntax_Highlighting#The_HSV_Color_Space
        # Yet to be perfected...
        h1, s1, v1, _ = color.getHsv()
        h2, s2, v2, _ = color.getHsv()
        if h1 == h2 == -1 and s1 == s2:
            # Lilely to be gray
            if v1 - v2 < 35:
                v1 = 255 if h2 < 128 else 0
                color = QtGui.QColor.fromHsv(h1, s1, v1)
                self.editor.logger.debug("Changing foreground color to %s" % str(color.getRgb()))  
        self.__foreground = color
    
    __background = QtGui.QColor()
    @property
    def background(self):
        return self.__background
    
    @background.setter
    def background(self, color):
        assert isinstance(color, QtGui.QColor)
        self.__background = color
    """
    
class BookmarkSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.bookmarkflagImage = resources.getImage("bookmarkflag")
        self.setFixedWidth(self.bookmarkflagImage.width())
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.repaint(self.rect())

    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowBookmarks_toggled(editor, checked):
            instance = editor.addonByClass(cls)
            instance.setVisible(checked)

        def on_actionShowBookmarks_testChecked(editor):
            instance = editor.addonByClass(cls)
            return instance.isVisible()
        
        baseMenu = ("View", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {'title': "Bookmarks",
            'callback': on_actionShowBookmarks_toggled,
            'shortcut': 'Alt+F10',
            'checkable': True,
            'testChecked': on_actionShowBookmarks_testChecked }
        return { baseMenu: menuEntry} 

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        page_bottom = self.editor.viewport().height()
       
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        
        while block.isValid():
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible() and block in self.editor.bookmarkListModel:
                painter.drawPixmap(0,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.bookmarkflagImage.height(),
                    self.bookmarkflagImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        self.editor.toggleBookmark(block)
        self.repaint(self.rect())
            
class FoldingSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.foldingcollapsedImage = resources.getImage("foldingcollapsed")
        self.foldingtopImage = resources.getImage("foldingtop")
        self.foldingbottomImage = resources.getImage("foldingbottom")
        self.setFixedWidth(self.foldingbottomImage.width())
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.repaint(self.rect())
    
    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowFoldings_toggled(editor, checked):
            instance = editor.addonByClass(cls)
            instance.setVisible(checked)

        def on_actionShowFoldings_testChecked(editor):
            instance = editor.addonByClass(cls)
            return instance.isVisible()
        
        baseMenu = ("View", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {'title': 'Foldings',
            'callback': on_actionShowFoldings_toggled,
            'shortcut': 'Shift+F10',
            'checkable': True,
            'testChecked': on_actionShowFoldings_testChecked }
        return {baseMenu: menuEntry} 

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        page_bottom = self.editor.viewport().height()
       
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        
        while block.isValid():
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                userData = block.userData()
    
                mark = self.editor.folding.getFoldingMark(block)
                if self.editor.folding.isStart(mark):
                    if userData.folded:
                        painter.drawPixmap(0,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingcollapsedImage.height(),
                            self.foldingcollapsedImage)
                    else:
                        painter.drawPixmap(0,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingtopImage.height(),
                            self.foldingtopImage)
                elif self.editor.folding.isStop(mark):
                    painter.drawPixmap(0,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingbottomImage.height(),
                        self.foldingbottomImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        if self.editor.folding.isFoldingMark(block):
            if self.editor.folding.isFolded(block):
                self.editor.codeFoldingUnfold(block)
            else:
                self.editor.codeFoldingFold(block)

class SelectionSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignRight
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(10)
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.themeChanged.connect(self.updateColours)
        self.editor.extraSelectionChanged.connect(self.on_editor_extraSelectionChanged)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.update()
    
    def on_editor_extraSelectionChanged(self):
        self.update()

    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowSelection_toggled(editor, checked):
            instance = editor.addonByClass(cls)
            instance.setVisible(checked)

        def on_actionShowSelection_testChecked(editor):
            instance = editor.addonByClass(cls)
            return instance.isVisible()
        
        baseMenu = ("View", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {'title': 'Selection',
            'callback': on_actionShowSelection_toggled,
            'shortcut': 'Shift+F10',
            'checkable': True,
            'testChecked': on_actionShowSelection_testChecked }
        return {baseMenu: menuEntry} 

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font)
        page_bottom = self.editor.viewport().height()
        
        lineHeight = font_metrics.height()

        scrollBar = self.editor.verticalScrollBar()
        if scrollBar.isVisible():
            rectRelation = float(scrollBar.height()) / float(self.editor.document().blockCount())
        else:
            rectRelation = lineHeight
        rectHeight = round(rectRelation) if rectRelation >= 1 else 1

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        viewport_offset = self.editor.contentOffset()

        for cursor in self.editor.extraSelectionCursorsByScope("selection"):
            y = round(cursor.block().blockNumber() * rectRelation)
            if rectRelation == lineHeight:
                y += viewport_offset.y()
            painter.fillRect(0, y, 10, rectHeight, self.editor.colours['selection'])

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        print block