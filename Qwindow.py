"""
File name: Qwindow.py

Creation Date: Sa 30 Jan 2021

Description:

"""

# Python Libraries
# -----------------------------------------------------------------------------

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget
# Local Application Modules
# -----------------------------------------------------------------------------




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1100, 1100)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1000, 1000)








