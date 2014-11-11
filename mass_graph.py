#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    import numpy as np
    
    import matplotlib
    matplotlib.rcParams['backend.qt4']='PySide'
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    
    from PySide.QtGui import *
    
    from main import Ui_Form
    
except Exception as e:
    print str(e)
    raise SystemExit

class MatplotlibWidget:
    def __init__(self, mainWidget):
        
        self.figure = Figure()
        self.figureCanvas = FigureCanvas(self.figure)
        
        self.axes = self.figure.add_subplot(111)
        
        font = {'family': 'Courier New'}
        self.axes.set_title(u'График веса', font)
        self.axes.set_xlabel(u'Дата', font)
        self.axes.set_ylabel(u'Вес, кг', font)
        self.axes.set_ylim((80.0, 130.0))
        
        mainWidget.verticalLayout.insertWidget(0, self.figureCanvas)

    def plot(self, x, y):
        self.axes.plot(x, y)
        self.figureCanvas.draw()

class MainWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.addClick)
        
        self.mplWidget = MatplotlibWidget(self)

    def addClick(self):
        x = np.linspace(-100.0, 100, 200)
        y = np.random.random(x.shape) * 10 + 100
        
        self.mplWidget.plot(x, y)

def main():
    app = QApplication(sys.argv)

    mainWidget = MainWidget()
    mainWidget.show()
     
    return sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print str(e)
