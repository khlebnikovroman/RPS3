# -*- coding: utf-8 -*-
"""
Simple example of subclassing GraphItem.
"""
import os

import pyqtgraph as pg
from pyqtgraph import ViewBox
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

pg.mkQApp()
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'untitled.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


# w = pg.GraphicsLayoutWidget(show=True)
# w.setWindowTitle('pyqtgraph example: CustomGraphItem')

class MainWindow(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.show()
        self.ui.spinBox.valueChanged.connect(self.changeTableSize)
        self.ui.pushButton.clicked.connect(self.buildGraph)

    def changeTableSize(self):
        s = self.ui.spinBox.value()
        self.ui.tableWidget.setRowCount(s)
        self.ui.tableWidget.setColumnCount(s)

    def buildGraph(self):
        adj = []
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range(self.ui.tableWidget.columnCount()):
                    print(type(self.ui.tableWidget.item(i, j)))
                    if int(self.ui.tableWidget.item(i, j).text()):
                        adj.append([i, j])

        print(adj)


print(11111111111111)


# v= w.addViewBox()
# v.setAspectLocked()


# print(type(v))


class Graph(pg.GraphItem):

    def __init__(self, ui):
        self.ui = ui
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        self.selectedPoint = None
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)

    def addPoint(self, pos):
        self.data["pos"] = np.append(self.data["pos"], [pos], axis=0)
        self.text.append("ssss")
        self.setTexts(self.text)
        self.setData(text=self.text, adj=self.data["adj"], pxMode=False, size=1, pos=self.data["pos"])

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()

    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):

        pg.GraphItem.setData(self, **self.data)
        for i, item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])

    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            return
        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.updateGraph()
        ev.accept()

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.addPoint(ev.pos())

    def paintAll(self):
        data = self.scatter.getData()
        newPos = np.vstack([data[0], data[1]]).transpose()
        symbolBrushs = [None] * len(data[0])
        g.setData(pos=newPos, adj=adj, size=1, pxMode=False, text=texts,
                  symbolBrush=symbolBrushs)
        self.updateGraph()

    def paintPoint(self, mypoint_index):
        data_list = self.scatter.data.tolist()
        print(data_list)
        data = self.scatter.getData()
        newPos = np.vstack([data[0], data[1]]).transpose()
        symbolBrushs = [None] * len(data[0])
        symbolBrushs[mypoint_index] = pg.mkBrush(color=(255, 0, 0))
        g.setPen(symbolBrushs)
        self.updateGraph()

    def clicked(self, scatter, pts):
        if self.ui.radioButton.isChecked():
            if self.selectedPoint == None:
                self.selectedPoint = pts[0].index()
                # self.paintPoint(self.selectedPoint)
                print(type(self.data["adj"][0]))
                print(self.data)
            else:
                self.data["adj"] = np.append(self.data["adj"], np.array([[self.selectedPoint, pts[0].index()]]), axis=0)
                self.updateGraph()
                self.selectedPoint = None
                pass
            if self.selectedPoint == None:
                # self.paintAll()
                pass
        if self.ui.radioButton_2.isChecked():
            # поиск путей

            pass
        if self.ui.radioButton_3.isChecked():
            # удаление
            selPoint = pts[0].index()
            self.data['pos'] = np.delete(self.data['pos'], selPoint, axis=0)
            adjToDelete = []
            print(self.data['adj'])
            for j, i in enumerate(self.data['adj']):
                if i[0] == selPoint or i[1] == selPoint:
                    adjToDelete.append(j)
            self.data['adj'] = np.delete(self.data['adj'], adjToDelete, axis=0)
            for j, i in enumerate(self.data['adj']):
                for k, kk in enumerate(i):
                    print(k, selPoint)
                    if kk > selPoint:
                        self.data['adj'][j][k] -= 1

            self.text.pop(selPoint)
            self.setTexts(self.text)
            print(self.data['pos'])
            print(self.data['adj'])
            print(self.text)
            print(adjToDelete)
            self.setData(text=self.text, adj=self.data["adj"], pxMode=False, size=1, pos=self.data["pos"])

            pass


win = MainWindow()

g = Graph(win.ui)
## Define positions of nodes
pos = np.array([
    [0, 0],
    [15, 0],
    [0, 10],
    [10, 10],
    [5, 5],
    [15, 5],
    [15, 15]
], dtype=float)

## Define the set of connections in the graph
adj = np.array([
    [0, 1],
    [1, 3],
    [3, 2],
    [2, 0],
    [1, 5],
    [3, 5],
    [6, 1]
])

## Define text to show next to each symbol
texts = ["Point %d" % i for i in range(7)]

## Update the graph
g.setData(pos=pos, adj=adj, size=1, pxMode=False, text=texts)

win.ui.plot.setAspectLocked()
win.ui.plot.addItem(g)
win.ui.plot.setMenuEnabled(enableMenu=False, enableViewBoxMenu='same')
win.ui.plot.setBackground('w')

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
