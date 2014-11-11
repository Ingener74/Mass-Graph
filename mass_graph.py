#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import QTimer, QDateTime

try:
    import numpy as np
    
    import matplotlib
    matplotlib.rcParams['backend.qt4']='PySide'
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    
    from PySide.QtGui import *
    
    from main import Ui_MainWidget
    from add import Ui_AddWidget
    from settings import Ui_Settings
    
except Exception as e:
    print str(e)
    raise SystemExit

class MassGraph:
    def __init__(self):
        pass

class SettingsWidget(QWidget, Ui_Settings):
    def __init__(self, mainWidget, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.downMassDoubleSpinBox.valueChanged.connect(mainWidget.setMassLimits)
        self.upMassDoubleSpinBox.valueChanged.connect(mainWidget.setMassLimits)

class AddWidget(QWidget, Ui_AddWidget):
    def __init__(self, parent=None):
        super(AddWidget, self).__init__(parent)
        self.setupUi(self)

        self.addMassPushButton.clicked.connect(self.addMass)
        
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.onTimeout)
        self.timer1.start(1000)
        
    def onTimeout(self):
        now = QDateTime.currentDateTime()
#         print 'date and time', now.toPython()
        self.dateTimeEdit.setDateTime(now)
        
    def addMass(self):
        print 'add mass ', self.massDoubleSpinBox.value()
        self.hide()

class MatplotlibWidget:
    def __init__(self, mainWidget, settingsWidget):
        
        self.settingsWidget = settingsWidget
        
        self.figure = Figure()
        self.figureCanvas = FigureCanvas(self.figure)
        
        self.axes = self.figure.add_subplot(111)
        
        font = {'family': 'Courier New'}
        self.axes.set_title(u'График веса', font)
        self.axes.set_xlabel(u'Дата', font)
        self.axes.set_ylabel(u'Вес, кг', font)
        self.setMassLimits()
        
        now1 = QDateTime.currentDateTime()
        self.x = [now1.addDays(i).toPython() for i in xrange(0, 64)]
        self.y = [100 + 5.*np.random.rand() for i,n in enumerate(self.x)]
        
        # %H:%M:%S - 
        self.axes.set_xticklabels([n.strftime('%d:%m:%Y') for i,n in enumerate(self.x)], rotation=15)
        
        self.axes.plot(self.x, self.y)
        
        mainWidget.verticalLayout.insertWidget(0, self.figureCanvas)

    def plot(self, x, y):
        self.axes.plot(x, y)
        self.figureCanvas.draw()
        
    def setMassLimits(self):
        self.axes.set_ylim((self.settingsWidget.downMassDoubleSpinBox.value(), self.settingsWidget.upMassDoubleSpinBox.value()))
        self.figureCanvas.draw()

class MainWidget(QWidget, Ui_MainWidget):
    """
    Main Window
    """
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.addMassPushButton.clicked.connect(self.addClick)
        self.settingsPushButton.clicked.connect(self.settingsClick)
        
        self.addWidget = AddWidget()
        self.settingsWidget = SettingsWidget(self)

        self.mplWidget = MatplotlibWidget(self, self.settingsWidget)

    def addClick(self):
        self.addWidget.show()
    
    def settingsClick(self):
        self.settingsWidget.show()
        
    def setMassLimits(self):
        self.mplWidget.setMassLimits()

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
