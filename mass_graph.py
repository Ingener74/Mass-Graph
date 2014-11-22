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

class BodyMassModel:
    def __init__(self):
        print 'Body mass model'

    def __add__(self, other):
        pass

class MassGraph:
    DATABASE_FILE_NAME = 'database.json'
    DATABASE_KEY_PATTERN = '%H:%M:%S-%d:%m:%Y'

    def __init__(self, matplotlibWidget):
        
        self.plotWidget = matplotlibWidget
        
        self.x = []
        self.y = []
        
        self.reload_date_base()

    def get_sorted_dates(self, date_base):
        date_times = []
        for i in sorted(date_base.keys()):
            date_times.append(datetime.datetime.strptime(i, self.DATABASE_KEY_PATTERN))
        return date_times

    def reload_date_base(self):
        self.json_data = json.load(open(self.DATABASE_FILE_NAME))
        
        self.x = []
        self.y = []
        
        for date_time_mass_key in sorted(self.get_sorted_dates(self.json_data)):
            self.x.append(date_time_mass_key)
            self.y.append(self.json_data[date_time_mass_key.strftime(self.DATABASE_KEY_PATTERN)])
        
        self.plotWidget.plot(self.x, self.y)

    def save_to_json(self, key, val):
        self.json_data[key.strftime(self.DATABASE_KEY_PATTERN)] = val
        with open(self.DATABASE_FILE_NAME, "w") as json_file:
            json.dump(self.json_data, json_file, indent=4, separators=(',', ':'))
            json_file.flush()
            json_file.close()

    def add_mass_to_graph(self, date_time, mass):
        self.save_to_json(date_time, mass)
        self.reload_date_base()

    def get_last_mass(self):
        return self.y[-1]

class SettingsWidget(QWidget, Ui_Settings):
    CONFIG_FILE_NAME = 'config.json'
    CONFIG_UP_MASS = 'up_mass'
    CONFIG_DOWN_MASS = 'down_mass'
    CONFIG_TIME_UNIT = 'time_unit'
    CONFIG_TIME = 'time'

    CONFIG_TIME_UNIT_DAY = 'day'
    CONFIG_TIME_UNIT_WEEK = 'week'
    CONFIG_TIME_UNIT_MONTH = 'month'

    TIME_INDEX_TO_UNITS = {0: CONFIG_TIME_UNIT_DAY, 1: CONFIG_TIME_UNIT_WEEK, 2: CONFIG_TIME_UNIT_MONTH}
    TIME_UNITS_TO_INDEX = {CONFIG_TIME_UNIT_DAY: 0, CONFIG_TIME_UNIT_WEEK: 1, CONFIG_TIME_UNIT_MONTH: 2}

    def __init__(self, mainWidget, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.json_data = json.load(open(self.CONFIG_FILE_NAME))
        
        self.upMassDoubleSpinBox.setValue(self.json_data[self.CONFIG_UP_MASS])
        self.downMassDoubleSpinBox.setValue(self.json_data[self.CONFIG_DOWN_MASS])
        self.timeSpinBox.setValue(self.json_data[self.CONFIG_TIME])
        self.timeUnitComboBox.setCurrentIndex(self.TIME_UNITS_TO_INDEX[self.json_data[self.CONFIG_TIME_UNIT]])
        
        self.downMassDoubleSpinBox.valueChanged.connect(mainWidget.set_mass_limits)
        self.downMassDoubleSpinBox.valueChanged.connect(self.down_mass_changed)
        
        self.upMassDoubleSpinBox.valueChanged.connect(mainWidget.set_mass_limits)
        self.upMassDoubleSpinBox.valueChanged.connect(self.up_mass_changed)
        
        self.timeSpinBox.valueChanged.connect(self.time_changed)
        
        self.timeUnitComboBox.currentIndexChanged.connect(self.time_unit_changed)

    def save_to_json(self, key, val):
        self.json_data[key] = val
        with open(self.CONFIG_FILE_NAME, "w") as json_file:
            json.dump(self.json_data, json_file, sort_keys=True, indent=4, separators=(',', ':'))

    def up_mass_changed(self, val):
        self.save_to_json(self.CONFIG_UP_MASS, val)

    def down_mass_changed(self, val):
        self.save_to_json(self.CONFIG_DOWN_MASS, val)

    def time_changed(self, time):
        self.save_to_json(self.CONFIG_TIME, time)

    def time_unit_changed(self, index):
        self.save_to_json(self.CONFIG_TIME_UNIT, self.TIME_INDEX_TO_UNITS[index])

class AddWidget(QWidget, Ui_AddWidget):
    def __init__(self, massGraph, parent=None):
        super(AddWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.massGraph = massGraph

        self.addMassPushButton.clicked.connect(self.add_mass)
        
        self.massDoubleSpinBox.setValue(massGraph.get_last_mass())
        
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.on_timeout)
        self.timer1.start(1000)
        
    def on_timeout(self):
        now = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(now)
        
    def add_mass(self):
        self.massGraph.add_mass_to_graph(self.dateTimeEdit.dateTime().toPython(), self.massDoubleSpinBox.value())
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
        self.set_mass_limits()
        
        mainWidget.verticalLayout.insertWidget(0, self.figureCanvas)

    def plot(self, x, y):
        self.line1 = self.axes.plot(x, y)
        self.axes.set_xticklabels([n.strftime('%d:%m:%Y') for i,n in enumerate(x)], rotation=15)
#         self.axes.clear()
        self.figureCanvas.draw()

    def set_mass_limits(self):
        self.axes.set_ylim((self.settingsWidget.downMassDoubleSpinBox.value(), self.settingsWidget.upMassDoubleSpinBox.value()))
        self.figureCanvas.draw()

class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.addMassPushButton.clicked.connect(self.addClick)
        self.settingsPushButton.clicked.connect(self.settingsClick)
        
        self.settingsWidget = SettingsWidget(self)

        self.mplWidget = MatplotlibWidget(self, self.settingsWidget)

        self.massGraph = MassGraph(self.mplWidget)
        
        self.addWidget = AddWidget(self.massGraph)

    def addClick(self):
        self.addWidget.show()

    def settingsClick(self):
        self.settingsWidget.show()

    def set_mass_limits(self):
        self.mplWidget.set_mass_limits()

def main():
    app = QApplication(sys.argv)

    main_widget = MainWidget()
    main_widget.show()

    return sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print str(e)
        print traceback.format_exc()
