from PyQt5 import QtWidgets, QtGui, Qt


class DefaultButton(QtWidgets.QPushButton):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtGui.QCursor(Qt.Qt.PointingHandCursor))
        self.setup()
        
    def setup(self):
        self.setObjectName('DefaultButton')
        with open('steam-trade/ui/components/buttons/DefaultButton/DefaultButton.qss') as style:
            self.setStyleSheet(style)
        