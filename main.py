# -*- coding: utf-8 -*-
"""
Simple example of subclassing GraphItem.
"""
import os

import pyqtgraph as pg
from PyQt5.QtWidgets import QTableWidgetItem
from pyqtgraph import ViewBox
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from algs import Dijkstra, Floyd

pg.mkQApp()
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'untitled.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


# w = pg.GraphicsLayoutWidget(show=True)
# w.setWindowTitle('pyqtgraph example: CustomGraphItem')

class MyDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        return QtGui.QDoubleSpinBox(parent, maximum=1000, decimals=3, buttonSymbols=QtGui.QSpinBox.NoButtons)


class MainWindow(TemplateBaseClass):
    def __init__(self):

        TemplateBaseClass.__init__(self)

        self.ui = WindowTemplate()

        self.ui.setupUi(self)
        self.show()
        delegate = MyDelegate()
        self.ui.tableWidget.setItemDelegate(delegate)
        self.ui.spinBox.valueChanged.connect(self.changeTableSize)
        self.ui.pushButton.clicked.connect(self.findWays)
        self.changeTableSize()

    def changeTableSize(self):
        s = self.ui.spinBox.value()
        self.ui.tableWidget.setRowCount(s)
        self.ui.tableWidget.setColumnCount(s)
        for i in range(s):
            self.ui.tableWidget.setItem(i, i, QTableWidgetItem(str(0)))
            self.ui.tableWidget.item(i, i).setFlags(QtCore.Qt.ItemIsSelectable)
        self.ui.spinBox_2.setMaximum(s)
        self.ui.spinBox_3.setMaximum(s)
        for i in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.horizontalHeader().setResizeMode(i, QtGui.QHeaderView.Stretch)
            self.ui.tableWidget.verticalHeader().setResizeMode(i, QtGui.QHeaderView.Stretch)

    def findWays(self):
        s = self.ui.spinBox.value()
        data = [[] for i in range(s)]
        for i in range(s):
            for j in range(s):
                try:
                    item = float(self.ui.tableWidget.item(i, j).text())
                except:
                    item = np.Inf
                data[i].append(item)
        print(data)
        start = self.ui.spinBox_2.value()
        finish = self.ui.spinBox_3.value()
        self.ui.label.setText("Кратчайший путь от вершины "+ str(start)+ "\nдо вершины " + str(finish)+ " равен "+ str(Dijkstra(s,start-1,finish-1,data)))




win = MainWindow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
