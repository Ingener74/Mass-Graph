#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as n
import matplotlib.pyplot as p
import sys
from PySide.QtGui import *
from main import Ui_Form

class MainWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.addClick)
        
    def addClick(self):
        print 'add mass value'

def main():
    app = QApplication(sys.argv)
    
    m = MainWidget()
    m.show()
    
    return sys.exit(app.exec_())

if __name__ == '__main__':
    main()