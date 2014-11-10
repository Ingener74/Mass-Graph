#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

subprocess.Popen(['pyside-rcc', 'res/resources.qrc', '-o', 'resources_rc.py'])
subprocess.Popen(['pyside-uic', 'res/main.ui', '-o', 'main.py'])