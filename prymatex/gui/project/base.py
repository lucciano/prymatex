#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.utils.tree import TreeNode
from prymatex.utils import plist
from prymatex import resources

"""
currentDocument: Documento actual en el editor
documents: lista de documentos o carpetas, no se muy bien, creo que son los grupos de tm
    {'expanded': True,
     'name': 'source',
     'regexFolderFilter': '!.*/(\\.[^/]*|CVS|_darcs|_MTN|\\{arch\\}|blib|.*~\\.nib|.*\\.(framework|app|pbproj|pbxproj|xcode(proj)?|bundle))$',
     'selected': True,
     'sourceDirectory': ''}
fileHierarchyDrawerWidth: en ancho de la docker de proyectos
metaData: Datos de los editores por cada documento abierto, es un diccionario indexado por la ruta del documento
    {'Classes/MDSettings.h': {'caret': {'column': 20, 'line': 52},
                                       'columnSelection': False,
                                       'firstVisibleColumn': 0,
                                       'firstVisibleLine': 4,
                                       'selectFrom': {'column': 15,
                                                      'line': 52},
                                       'selectTo': {'column': 33,
                                                    'line': 52}},
openDocuments: Documentos abiertos en el editor es una lista, cada entrada de aca tiene una en metaData
showFileHierarchyDrawer: Mostrar la docker
windowFrame: El Tampaño del a ventana de projecto en tm
"""

class FileSystemTreeNode(TreeNode):
    @property
    def path(self):
        return os.path.join(self.parent.path, self.name)
    
    @property
    def isdir(self):
        return os.path.isdir(self.path)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class PMXProject(FileSystemTreeNode):
    KEYS = [    'currentDocument', 'documents', 'fileHierarchyDrawerWidth', 'metaData', 'openDocuments', 'showFileHierarchyDrawer', 'windowFrame' ]
    def __init__(self, name, directory, filePath, hash):
        FileSystemTreeNode.__init__(self, name)
        self.directory = directory
        self.filePath = filePath
        self.workingSet = None
        self.manager = None
        self.load(hash)
        
    def load(self, hash):
        for key in PMXProject.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = {}
        for key in PMXProject.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash

    def save(self):
        file = os.path.join(self.filePath)
        plist.writePlist(self.hash, file)

    def delete(self, removeFiles = False):
        os.unlink(os.path.join(self.filePath))
        if hard:
            try:
                os.rmdir(self.directory)
            except os.OSError:
                pass

    def buildEnvironment(self):
        env = {}
        env['TM_PROJECT_DIRECTORY'] = self.directory
        env['TM_SELECTED_FILES'] = ""
        env['TM_SELECTED_FILE'] = ""
        return env

    @classmethod
    def loadProject(cls, filePath, manager):
        name = os.path.splitext(os.path.basename(filePath))[0]
        directory = os.path.dirname(filePath)
        try:
            data = plist.readPlist(filePath)
            project = cls(name, directory, filePath, data)
            manager.addProject(project)
        except Exception, e:
            print "Error in project %s (%s)" % (filePath, e)
    
    def setManager(self, manager):
        self.manager = manager
    
    def setWorkingSet(self, workingSet):
        self.workingSet = set

    @property
    def path(self):
        return self.directory

    @property
    def icon(self):
        if self.manager.isOpen(self):
            return resources.getIcon("projectopen")
        else:
            return resources.getIcon("projectclose")

    def findDirectoryNode(self, path):
        current = self
        for part in path.split(os.path.sep):
            nodes = filter(lambda node: node.isdir and node.name == part, current.children)
            assert len(nodes) <= 1, "More than one node"
            #TODO: Arregrlar el detalle del split con cadena vacia
            if len(nodes):
                current = nodes.pop()
        return current
        