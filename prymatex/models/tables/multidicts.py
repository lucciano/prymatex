#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

class SelectableMultiDictTableModel(QtCore.QAbstractTableModel):
    dictionaryChanged = QtCore.pyqtSignal(str)
    COLUMN_NAMES = 0
    COLUMN_VALUES = 1
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.dictionaries = []

    def dictionaryNames(self):
        return map(lambda d: d["name"], self.dictionaries)


    def dictionaryByName(self, name):
        for dictionary in self.dictionaries:
            if dictionary['name'] == name:
                return dictionary


    def addDictionary(self, name, data, editable = False, selectable = False, visible = True):
        if hasattr(data, "iteritems") and callable(data.iteritems):
            data = map(lambda (name, value): {'name': name, 'value': value, 'selected': True}, data.iteritems())
            selectable = False
        dictionary = {
            'name': name,
            'data': data,
            'editable': editable,
            'selectable': selectable,
            'visible': visible
        }
        self.dictionaries.append(dictionary)
        self.layoutChanged.emit()

    
    def clear(self):
        self.changes = {}
        self.selected = {}
        self.dictionaries = []
        self.layoutChanged.emit()


    def isVisible(self, name):
        dictionary = self.dictionaryByName(name)
        return dictionary and dictionary['visible']


    def setVisible(self, name, visible):
        dictionary = self.dictionaryByName(name)
        dictionary['visible'] = visible
        self.layoutChanged.emit()

        
    def __mapToDictionary(self, index):
        currentDict = None
        for currentDict in self.dictionaries:
            if currentDict["visible"]:
                varCount = len(currentDict['data'])
                if index < varCount:
                    break
                index -= varCount
        return index, currentDict


    def __mapToPosition(self, dictionary, top = True):
        position = 0
        for currentDict in self.dictionaries:
            if currentDict["visible"]:
                if currentDict == dictionary:
                    break
                position += len(currentDict['data'])
        if not top:
            position += len(currentDict['data'])
        return position


    def dictionaryData(self, name, raw = False):
        dictionary = self.dictionaryByName(name)
        if dictionary:
            data = dictionary["data"]
            if raw:
                return data[:]
            return dict(map(lambda value: (value["name"], value["value"]),
                filter(lambda value: value["selected"], dictionary["data"])))

    
    def get_value(self, index):
        row, dictionary = self.__mapToDictionary(index.row())
        value = dictionary["data"][row][index.column() == self.COLUMN_NAMES and "name" or "value"]
        selected = dictionary["data"][row]["selected"]
        return value, selected, dictionary

        
    def rowCount(self, parent = None):
        if not self.dictionaries:
            return 0
        return reduce(lambda count, dictionary: count + (dictionary['visible'] and len(dictionary['data']) or 0), self.dictionaries, 0)


    def columnCount(self, parent = None):
        return 2

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        value, selected, dictionary = self.get_value(index)
        if role == QtCore.Qt.CheckStateRole and index.column() == 0 and dictionary['selectable']:
            return QtCore.Qt.Unchecked if not selected else QtCore.Qt.Checked
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            return value

        
    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el cambio, falso en caso contrario"""

        if not index.isValid(): return False
        row, dictionary = self.__mapToDictionary(index.row())

        if role == QtCore.Qt.EditRole:
            dictionary["data"][row]["value"] = value
            self.dataChanged.emit(index, index)
            self.dictionaryChanged.emit(dictionary["name"])
            return True
        elif role == QtCore.Qt.CheckStateRole:
            dictionary["data"][row]["selected"] = value == QtCore.Qt.Checked
            self.dataChanged.emit(index, index)
            self.dictionaryChanged.emit(dictionary["name"])
            return True
        return False

        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Name"
                elif section == 1:
                    return "Value"


    def hasItem(self, dictionaryName, itemName):
        dictionary = self.dictionaryByName(dictionaryName)
        return any(map(lambda item: item["name"] == itemName, dictionary["data"]))


    def insertItem(self, dictionaryName, itemName):
        dictionary = self.dictionaryByName(dictionaryName)
        if dictionary is not None and dictionary['editable']:
            position = self.__mapToPosition(dictionary)
            self.beginInsertRows(QtCore.QModelIndex(), position, position)
            dictionary['data'].insert(0, {'name': itemName, 'value': "", 'selected': dictionary['selectable']})
            self.endInsertRows()
            self.dictionaryChanged.emit(dictionaryName)


    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        row, dictionary = self.__mapToDictionary(position)
        if not dictionary["editable"]:
            return False
        for _ in range(rows):
            dictionary['data'].pop(row)
        self.endRemoveRows()
        self.dictionaryChanged.emit(dictionary["name"])
        return True


    def flags(self, index):
        row, dictionary = self.__mapToDictionary(index.row())
        flags = QtCore.QAbstractTableModel.flags(self, index)
        if dictionary['selectable']:
            flags |= QtCore.Qt.ItemIsUserCheckable
        if dictionary['editable'] and index.column() == 1:
            flags |= QtCore.Qt.ItemIsEditable            
        return flags