'''
This module is inspired in QtCretor FileManager instance
'''

import os, codecs
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.core.exceptions import APIUsageError, PrymatexIOException

class PMXFileManager(PMXObject):
    ''' A File Manager
    '''
    fileOpened = QtCore.pyqtSignal()
    fileHistoryChanged = QtCore.pyqtSignal()
    
    class Meta:
        settings = 'filemanager'

    fileHistory = pmxConfigPorperty(default=[])
    fileHistoryLength = pmxConfigPorperty(default=10)

    def __init__(self, parent):
        super(PMXFileManager, self).__init__(parent)

        self.opened_files = {}
        self.new_file_counter = 0
        self.iconProvider = QtGui.QFileIconProvider()
        self.configure()

    def _add_file_history(self, fileInfo):
        path = fileInfo.absoluteFilePath()
        if path not in self.fileHistory:
            self.fileHistory.insert(0, path)
        if len(self.fileHistory) > self.fileHistoryLength:
            self.fileHistory = self.fileHistory[0:self.fileHistoryLength]
        self.fileHistoryChanged.emit()
        
    def openFile(self, fileInfo):
        """Open and read a file, return the content."""
        if not fileInfo.exists():
            raise PrymatexIOException("The file does not exist")
        if not fileInfo.isFile():
            raise PrymatexIOException("%s is not a file" % fileInfo)
        f = QtCore.QFile(fileInfo.absoluteFilePath())
        if not f.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
            raise PrymatexIOException("%s" % f.errorString())
        stream = QtCore.QTextStream(f)
        content = stream.readAll()
        f.close()
        #Update file history
        self._add_file_history(fileInfo)
        return content
    
    def saveFile(self, fileInfo, content):
        """Function that actually save the content of a file (thread)."""
        try:
            f = QtCore.QFile(fileInfo.absoluteFilePath())
            if not f.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Truncate):
                raise PrymatexIOException(f.errorString())
            stream = QtCore.QTextStream(f)
            encoded_stream = stream.codec().fromUnicode(content)
            f.write(encoded_stream)
            f.flush()
            f.close()
        except:
            raise
    
    @property
    def currentDirectory(self):
        #TODO: el ultimo directorio o algo de eso :)
        return os.path.expanduser("~") 

    def getNewFile(self):
        ''' Returns a new QFileInfo '''
        path = os.path.join(self.currentDirectory, "untitled %d" % self.new_file_counter)
        self.new_file_counter += 1
        return QtCore.QFileInfo(path)
        
    def getOpenFiles(self):
        names = QtGui.QFileDialog.getOpenFileNames(None, "Open Files", self.currentDirectory)
        return map(lambda name: QtCore.QFileInfo(name), names)
    
    def getSaveFile(self, fileInfo = None, title = "Save file", filters = []):
        if fileInfo is None:
            fileInfo = QtCore.QFileInfo(self.currentDirectory)
        filters = ";;".join(filters)
        name = QtGui.QFileDialog.getSaveFileName(None, title, fileInfo.absoluteFilePath(), filters)
        if name is not None:
            return QtCore.QFileInfo(name)
    
    def getFileIcon(self, fileInfo):
        if fileInfo.exists():
            return self.iconProvider.icon(fileInfo)
        return self.iconProvider.icon(QtGui.QFileIconProvider.File)
    
    def getFileType(self, fileInfo):
        return self.iconProvider.type(fileInfo)
    
