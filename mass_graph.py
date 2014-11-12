#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import datetime
import traceback

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

class DataBase:
    def __init__(self):
        pass

class MassGraph:
    DATABASE_FILE_NAME   = 'database.json'
    DATABASE_KEY_PATTERN = '%H:%M:%S-%d:%m:%Y'

    def __init__(self, matplotlibWidget):
        
        self.plotWidget = matplotlibWidget
        
        self.json_data = json.load(open(self.DATABASE_FILE_NAME))
        
        self.x = []
        self.y = []
        
        self.reloadDateBase()

    def reloadDateBase(self):
        for date_time_mass_key in self.json_data.keys():
            self.x.append(datetime.datetime.strptime(date_time_mass_key, self.DATABASE_KEY_PATTERN))
            self.y.append(self.json_data[date_time_mass_key])
            
        self.plotWidget.plot(self.x, self.y)

    def saveToJson(self, key, val):
        self.json_data[key.strftime(self.DATABASE_KEY_PATTERN)] = val
        with open(self.DATABASE_FILE_NAME, "w") as json_file:
            json.dump(self.json_data, json_file, sort_keys=True, indent=4, separators=(',', ':'))

    def addMassToGraph(self, date_time, mass):
        self.saveToJson(date_time, mass)
        self.reloadDateBase()
        
    def getLastMass(self):
        return self.y[-1]

class SettingsWidget(QWidget, Ui_Settings):
    CONFIG_FILE_NAME = 'config.json'
    CONFIG_UP_MASS   = 'up_mass'
    CONFIG_DOWN_MASS = 'down_mass'
    CONFIG_TIME_UNIT = 'time_unit'
    CONFIG_TIME      = 'time'
    
    CONFIG_TIME_UNIT_DAY   = 'day'
    CONFIG_TIME_UNIT_WEEK  = 'week'
    CONFIG_TIME_UNIT_MONTH = 'month'
    
    TIME_UNITS = {0: CONFIG_TIME_UNIT_DAY, 1: CONFIG_TIME_UNIT_WEEK, 2: CONFIG_TIME_UNIT_MONTH}
    
    def __init__(self, mainWidget, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.json_data = json.load(open(self.CONFIG_FILE_NAME))
        
        self.upMassDoubleSpinBox.setValue(self.json_data[self.CONFIG_UP_MASS])
        self.downMassDoubleSpinBox.setValue(self.json_data[self.CONFIG_DOWN_MASS])
        
        time_unit = self.json_data[self.CONFIG_TIME_UNIT]
        if time_unit == self.CONFIG_TIME_UNIT_DAY:
            self.timeUnitComboBox.setCurrentIndex(0)
        elif time_unit == self.CONFIG_TIME_UNIT_WEEK:
            self.timeUnitComboBox.setCurrentIndex(1)
        elif time_unit == self.CONFIG_TIME_UNIT_MONTH:
            self.timeUnitComboBox.setCurrentIndex(2)
        else:
            raise ValueError('time unit: day, week, month')
        
        self.timeSpinBox.setValue(self.json_data[self.CONFIG_TIME])
        
        self.downMassDoubleSpinBox.valueChanged.connect(mainWidget.setMassLimits)
        self.downMassDoubleSpinBox.valueChanged.connect(self.downMassChanged)
        
        self.upMassDoubleSpinBox.valueChanged.connect(mainWidget.setMassLimits)
        self.upMassDoubleSpinBox.valueChanged.connect(self.upMassChanged)
        
        self.timeUnitComboBox.currentIndexChanged.connect(self.timeUnitChanged)
        
    def saveToJson(self, key, val):
        self.json_data[key] = val
        with open(self.CONFIG_FILE_NAME, "w") as json_file:
            json.dump(self._json_data, json_file, sort_keys=True, indent=4, separators=(',', ':'))

    def upMassChanged(self, val):
        self.saveToJson(self.CONFIG_UP_MASS, val)
    
    def downMassChanged(self, val):
        self.saveToJson(self.CONFIG_DOWN_MASS, val)
        
    def timeUnitChanged(self, index):
        print 'time unit', self.TIME_UNITS[index]

class AddWidget(QWidget, Ui_AddWidget):
    def __init__(self, parent=None):
        super(AddWidget, self).__init__(parent)
        self.setupUi(self)

        self.addMassPushButton.clicked.connect(self.addMass)
        
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.onTimeout)
        self.timer1.start(1000)
        
    def onTimeout(self):
        self.now = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(self.now)
        
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
        
        # %H:%M:%S - n.strftime('%d:%m:%Y')
        self.axes.set_xticklabels([n.strftime('%d:%m:%Y') for i,n in enumerate(self.x)], rotation=15)
        
        self.axes.plotWidget(self.x, self.y)
        
        mainWidget.verticalLayout.insertWidget(0, self.figureCanvas)
        
    def plotWidget(self, x, y):
        self.axes.plotWidget(x, y)
        self.figureCanvas.draw()
        
    def setMassLimits(self):
        self.axes.set_ylim((self.settingsWidget.downMassDoubleSpinBox.value(), self.settingsWidget.upMassDoubleSpinBox.value()))
        self.figureCanvas.draw()

class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.addMassPushButton.clicked.connect(self.addClick)
        self.settingsPushButton.clicked.connect(self.settingsClick)
        
        self.addWidget = AddWidget()
        self.settingsWidget = SettingsWidget(self)

        self.mplWidget = MatplotlibWidget(self, self.settingsWidget)

        self.massGraph = MassGraph(self.mplWidget)

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
        print traceback.format_exc()
