#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
from prymatex.qt import QtCore, QtGui

from prymatex.models.properties import PropertyTreeNode
from prymatex.ui.configure.resource import Ui_ResouceWidget

class ResoucePropertiesWidget(QtGui.QWidget, PropertyTreeNode, Ui_ResouceWidget):
    """Resouce"""
    NAMESPACE = ""
    TITLE = "Resouce"

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PropertyTreeNode.__init__(self, "resouce")
        self.setupUi(self)
        self.fileSystemItem = None

    def acceptFileSystemItem(self, fileSystemItem):
        return True
    
    def edit(self, fileSystemItem):
        self.fileSystemItem = fileSystemItem
        self.textLabelPath.setText(self.fileSystemItem.relpath())
        self.textLabelType.setText(self.fileSystemItem.type())
        self.textLabelLocation.setText(self.fileSystemItem.path())
        self.textLabelSize.setText("%d bytes" % self.fileSystemItem.size())
        self.textLabelLastModified.setText(self.fileSystemItem.path())
        self.updatePermissions(self.fileSystemItem.path())

    def updatePermissions(self, path):
        # TODO: Usar el file manager?
        # S_IRWXU 00700   mask for file owner permissions
        # S_IRUSR 00400   owner has read permission
        # S_IWUSR 00200   owner has write permission
        # S_IXUSR 00100   owner has execute permission
        # S_IRWXG 00070   mask for group permissions
        # S_IRGRP 00040   group has read permission
        # S_IWGRP 00020   group has write permission
        # S_IXGRP 00010   group has execute permission
        # S_IRWXO 00007   mask for permissions for others (not in group)
        # S_IROTH 00004   others have read permission
        # S_IWOTH 00002   others have write permission
        # S_IXOTH 00001   others have execute permission
        st = os.stat(path)
        bool(st.st_mode & stat.S_IRGRP)
        os.access(path, os.F_OK)
        os.access(path, os.R_OK)
        os.access(path, os.W_OK)
        os.access(path, os.X_OK)