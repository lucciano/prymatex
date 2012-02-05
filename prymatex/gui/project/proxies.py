#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import fnmatch

from PyQt4 import QtCore, QtGui

from prymatex.gui.project.base import PMXProject

class PMXProjectTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.application = QtGui.QApplication.instance()
        self.orderBy = "name"
        self.folderFirst = True
        self.descending = False
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(sIndex)
        if node.isproject: return True
        #TODO: Esto depende de alguna configuracion tambien
        if node.ishidden: return False
        if node.isdir: return True
        
        regexp = self.filterRegExp()        
        if not regexp.isEmpty():
            pattern = regexp.pattern()
            #TODO: Hacerlo en el fileManager
            match = any(map(lambda p: fnmatch.fnmatch(node.path, p), map(lambda p: p.strip(), pattern.split(","))))
            return not match
        return True

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def lessThan(self, left, right):
        isleftdir = self.sourceModel().isDir(left)
        isrightdir = self.sourceModel().isDir(right)
        if self.folderFirst and isleftdir and not isrightdir:
            return not self.descending
        elif self.folderFirst and not isleftdir and isrightdir:
            return self.descending
        else:
            leftPath = self.sourceModel().filePath(left)
            rightPath = self.sourceModel().filePath(right)
            return self.application.fileManager.compareFiles(leftPath, rightPath, self.orderBy)

    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
    
    def refresh(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().refresh(sIndex)
    
    def indexForPath(self, path):
        sIndex = self.sourceModel().indexForPath(path)
        if sIndex.isValid():
            return self.mapFromSource(sIndex)
        return sIndex
        
    def filePath(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().filePath(sIndex)
    
    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        self.descending = descending
        QtGui.QSortFilterProxyModel.sort(self, 0, order)
        
    def isDir(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().isDir(sIndex)

    #=======================================================
    # Drag and Drop support
    #=======================================================
    def flags(self, index):
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        if not self.isDir(index):
            return defaultFlags | QtCore.Qt.ItemIsDragEnabled 
        return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
            
    def dropMimeData(self, mimeData, action, row, col, parentIndex):
        return False
    
    def mimeTypes(self):
        return ["text/uri-list"]
        
    def mimeData(self, indexes):
        urls = map(lambda index: QtCore.QUrl.fromLocalFile(self.filePath(index)), indexes)
        print urls
        mimeData = QtCore.QMimeData()
        mimeData.setUrls(urls)
        return mimeData