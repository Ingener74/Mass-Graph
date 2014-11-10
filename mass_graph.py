#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc

import numpy as np
import sympy as sm

import sys

from PySide.QtGui import *
from main import Ui_Form

font = {'family': 'Courier New', 'weight':'normal'}
rc('font', **font)

class MatplotlibWidget:
    def __init__(self, mainWidget):
        
        self.figure = Figure()
        self.figureCanvas = FigureCanvas(self.figure)
        
        self.axes = self.figure.add_subplot(111)
        
        mainWidget.verticalLayout.insertWidget(0, self.figureCanvas)
        
    def plot(self, x, y):
        self.axes.set_xlabel(u'Дата')
        self.axes.set_ylabel(u'Вес, кг')
#         self.axes.set_axes([-100.0, 100.0, 0.0, 100.0])
        self.axes.plot(x, y)
        self.figureCanvas.draw()

class MainWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.addClick)
        
        self.mplWidget = MatplotlibWidget(self)
        
        x = sm.Symbol('x')
        s1 = (1 - 2*x) * (3 + x) + x**2
        print u'упрощённое выражение ', sm.simplify(s1)
        
    def addClick(self):
        x = np.linspace(-100.0, 100, 200)
#         y = np.sin(x)
        y = np.random.random(x.shape)

        self.mplWidget.plot(x, y)

        pass

def main():
    app = QApplication(sys.argv)
     
    m = MainWidget()
    m.show()
     
    return sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print str(e)
