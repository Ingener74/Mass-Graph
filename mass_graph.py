#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as n
import matplotlib.pyplot as p
import subprocess as s
import os
import sys
from PySide.QtGui import *
from main import Ui_Form

class MainWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)

def main():
    if not os.path.exists('resources_rc.py'): s.Popen('pyside-rcc res/resources.qrc -o resources_rc.py')
    if not os.path.exists('main.py'):         s.Popen('pyside-uic res/main.ui -o main.py')
    
    app = QApplication(sys.argv)
    
    m = MainWidget()
    m.show()
    
    return sys.exit(app.exec_())

if __name__ == '__main__':
    main()