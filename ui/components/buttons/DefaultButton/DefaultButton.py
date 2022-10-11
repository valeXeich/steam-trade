from pathlib import Path

from PyQt5 import QtWidgets, QtGui, Qt


class DefaultButton(QtWidgets.QPushButton):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self.setup()
        
    # def setup(self):
    #     self.setObjectName('DefaultButton')
    #     with open(f'{Path(__file__).parent}/DefaultButton.qss') as style:
    #         self.setStyleSheet(style)
        