from PyQt4.QtGui import QWidget, QPainter, QPixmap, QFontMetrics
from PyQt4.Qt import QColor, QSize
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.editor.syntax import PMXBlockUserData
from prymatex import res_rc
from prymatex.core.base import PMXObject

#based on: http://john.nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/ (MIT license)
class PMXSidebar(QWidget, PMXObject):
    foreground = pmxConfigPorperty(default = QColor(170, 170, 170))
    background = pmxConfigPorperty(default = QColor(227, 227, 227))
    
    def __init__(self, editor):
        super(PMXSidebar, self).__init__(editor)
        self.editor = editor
        self.highest_line = 0
        self.bookmarkArea = 12
        self.foldArea = 12
        self.foldingTopIcon = QPixmap()
        self.foldingTopIcon.load(":/sidebar/resources/sidebar/folding-top.png")
        self.foldingBottomIcon = QPixmap()
        self.foldingBottomIcon.load(":/sidebar/resources/sidebar/folding-bottom.png")
        self.foldingCollapsedIcon = QPixmap()
        self.foldingCollapsedIcon.load(":/sidebar/resources/sidebar/folding-collapsed.png")
        self.bookmarkFlagIcon = QPixmap()
        self.bookmarkFlagIcon.load(":/sidebar/resources/sidebar/bookmark-flag.png")
        self.configure()

    class Meta(object):
        settings = 'editor.sidebar'
        
    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())

        painter = QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        line_count = block.blockNumber()
        painter.setPen(self.foreground)
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            font = painter.font()
            font.setBold(block == current_block)
            painter.setFont(font)

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            if block.isVisible():
                painter.drawText(self.width() - self.foldArea - font_metrics.width(str(line_count)) - 3,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - 1,
                    str(line_count))

                #Bookmarks
                if line_count in self.editor.bookmarks:
                    painter.drawPixmap(1,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.bookmarkFlagIcon.height(),
                        self.bookmarkFlagIcon)
    
                user_data = block.userData()
                if user_data != None:
                    if user_data.folding == PMXBlockUserData.FOLDING_START:
                        if line_count in self.editor.folded:
                            painter.drawPixmap(self.width() - self.foldingCollapsedIcon.width() - 1,
                                round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingCollapsedIcon.height(),
                                self.foldingCollapsedIcon)
                        else:
                            painter.drawPixmap(self.width() - self.foldingTopIcon.width() - 1,
                                round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingTopIcon.height(),
                                self.foldingTopIcon)
                    elif user_data.folding == PMXBlockUserData.FOLDING_STOP:
                        painter.drawPixmap(self.width() - self.foldingCollapsedIcon.width() - 1,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingCollapsedIcon.height(),
                            self.foldingBottomIcon)
            
            block = block.next()

        self.highest_line = line_count

        painter.end()
        QWidget.paintEvent(self, event)

    def mousePressEvent(self, event):
        xofs = self.width() - self.foldArea
        xobs = self.bookmarkArea
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        fh = font_metrics.lineSpacing()
        ys = event.posF().y()
        lineNumber = 0

        if event.pos().x() > xofs or event.pos().x() < xobs:
            block = self.editor.firstVisibleBlock()
            viewport_offset = self.editor.contentOffset()
            page_bottom = self.editor.viewport().height()
            while block.isValid():
                position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
                if position.y() > page_bottom:
                    break
                if position.y() < ys and (position.y() + fh) > ys:
                    lineNumber = block.blockNumber() + 1
                    break
                block = block.next()
            if event.pos().x() > xofs:
                self.editor.codeFoldingEvent(lineNumber)
            else:
                self.editor.toggleBookmark(lineNumber)

"""
class PMXSideArea(QWidget):
    foreground = Setting(default = QColor(170, 170, 170))
    background = Setting(default = QColor(227, 227, 227))
    
    def __init__(self, editor):
        super(PMXSideArea, self).__init__(editor)
        self.editor = editor
    
    class Meta:
        setting = "editor.sidebar"
    
    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)
    
    def paintEvent(self, event):
        self.lineNumberAreaPaintEvent(event)
        
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.background)
        
        block = self.editor.firstVisibleBlock()
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())
        
        blockNumber = block.blockNumber()
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top < event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(self.foreground)
                font = painter.font()
                font.setBold(block == current_block)
                painter.setFont(font)
                painter.drawText(-7, top, self.width(), self.fontMetrics().height(), Qt.AlignRight, number)
                    
            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            blockNumber += 1
            
        painter.end()
        super(PMXSideArea, self).paintEvent(event)
"""