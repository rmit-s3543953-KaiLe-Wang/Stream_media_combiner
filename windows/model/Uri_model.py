'''
Created on Jul 7, 2020

@author: kai
'''
from PyQt5 import QtCore

class Uri_model(QtCore.QAbstractTableModel):
    def __init__(self,data,parent=None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.items=data     # Initial Data

    def rowCount( self, parent ):
        return len(self.items)

    def columnCount( self , parent ):
        return max(len(self.items[x]) for x in range(len(self.items)))

    def data ( self , index , role ):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.items[row][column]
            return str(value)

    def setData(self, index, value):
        self.items[index.row()][index.column()] = value
        return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsSelectable      

    def insertRows(self , position , rows , item , parent=QtCore.QModelIndex()):
        # beginInsertRows (self, QModelIndex parent, int first, int last)
        self.beginInsertRows(QtCore.QModelIndex(),len(self.items),len(self.items)+1)
        self.items.append(item) # Item must be an array
        self.endInsertRows()
        return True