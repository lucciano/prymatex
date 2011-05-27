from PyQt4.Qt import *


class OverlayedTestWidget(QWidget):
    rectStart = None
    rectEnd = None
    
    def __init__(self):
        super(OverlayedTestWidget, self).__init__()
        self.setWindowTitle("Drag mouse over me")
    
    def mousePressEvent(self, event):
        super(OverlayedTestWidget, self).mousePressEvent(event)
        pos = event.pos()
        #print "Mouse press", pos 
        self.rectStart = pos
        
    def mouseMoveEvent(self, event):
        super(OverlayedTestWidget, self).mouseMoveEvent(event)
        pos = event.pos()
        #print "Mouse move", pos
        #print "Mouse drag"
        self.rectEnd = pos
        self.repaint()
        self.update()
        
        
    def mouseReleaseEvent(self, event):
        # Esto no fuciona si es una ABC :(
        super(OverlayedTestWidget, self).mouseReleaseEvent(event)
        #print "Mouse release", event.pos()
        self.rectStart = self.rectEnd = None
        #self.repaint(self.viewport().geometry())
        #self.re
        self.update()
    
    def paintEvent(self, event):
        print 
        retval = super(OverlayedTestWidget, self).paintEvent(event)
        
        #print self.rectStart, self.rectEnd
        
        if self.rectStart and self.rectEnd:
            #print "printing"
            if isinstance(self, QAbstractScrollArea):
                painter = QPainter(self.viewport())
                painter.translate(-self.horizontalScrollBar().value(), 
                              -self.verticalScrollBar().value())
            
            else:
                painter = QPainter(self)
            
            
            
            pen = QPen("red")
            pen.setWidth(2)
            painter.setPen(pen)
            
            color = QColor()
            color.setAlpha(128)
            painter.setBrush(QBrush(color))
            painter.setOpacity(0.2)
            painter.drawRect(QRect(self.rectStart, self.rectEnd))
            
            #painter.end()
            
        return retval
    

class OverlayedQTextEdit(QPlainTextEdit):
    rectStart = None
    rectEnd = None
    
    def __init__(self):
        super(OverlayedQTextEdit, self).__init__()
        self.setWindowTitle("Drag mouse over me")
        self.setPlainText('\n'*10)
    
    def mousePressEvent(self, event):
        super(OverlayedQTextEdit, self).mousePressEvent(event)
        pos = event.pos()
        #print "Mouse press", pos 
        self.rectStart = pos
        
    def mouseMoveEvent(self, event):
        super(OverlayedQTextEdit, self).mouseMoveEvent(event)
        pos = event.pos()
        #print "Mouse move", pos
        #print "Mouse drag"
        self.rectEnd = pos
        self.repaint()
        self.update()
        
        
    def mouseReleaseEvent(self, event):
        # Esto no fuciona si es una ABC :(
        super(OverlayedQTextEdit, self).mouseReleaseEvent(event)
        #print "Mouse release", event.pos()
        self.rectStart = self.rectEnd = None
        #self.repaint(self.viewport().geometry())
        #self.re
        self.update()
    
    def paintEvent(self, event):
        print 
        retval = super(OverlayedQTextEdit, self).paintEvent(event)
        
        #print self.rectStart, self.rectEnd
        
        if self.rectStart and self.rectEnd:
            #print "printing"
            if isinstance(self, QAbstractScrollArea):
                painter = QPainter(self.viewport())
                painter.translate(-self.horizontalScrollBar().value(), 
                              -self.verticalScrollBar().value())
            
            else:
                painter = QPainter(self)
            
            
            
            pen = QPen("red")
            pen.setWidth(2)
            painter.setPen(pen)
            
            color = QColor()
            color.setAlpha(128)
            painter.setBrush(QBrush(color))
            painter.setOpacity(0.2)
            painter.drawRect(QRect(self.rectStart, self.rectEnd))
            
            #painter.end()
            
        return retval




class TestWidget(QWidget):
    def __init__(self):
        super(TestWidget, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('''
        Palying with overlay
        '''.strip()))
        btn = QPushButton("QWidget")
        btn.pressed.connect(self.showWidget)
        layout.addWidget(btn)
        
        btn = QPushButton("QPlainTextEdit")
        layout.addWidget(btn)
        btn.pressed.connect(self.showTextEdit)
        self.setLayout(layout)
        
    def showWidget(self):
        if not hasattr(self, 'testWidget'):
            self.testWidget = OverlayedTestWidget()
        self.testWidget.show()
    
    def showTextEdit(self):
        if not hasattr(self, 'testTextEdit'):
            self.testTextEdit = OverlayedQTextEdit()
        self.testTextEdit = OverlayedQTextEdit()
        self.testTextEdit.show()
            

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = TestWidget()
    
    win.show()
    win.setWindowTitle("Test")
    sys.exit(app.exec_())
    