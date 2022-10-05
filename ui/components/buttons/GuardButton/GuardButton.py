from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GuardButton(DefaultButton):
    def __init__(self, state, parent=None):
        self.state = state
        super().__init__(parent)
    
    def setup(self):
        path = Path(__file__).parent
        self.setObjectName('GuardButton')
        
        if not self.state:
            img_path = f'{path.parent.parent.parent}/assets/guard_add.png'
        else:
            img_path = f'{path.parent.parent.parent}/assets/guard_remove.png'
            
        with open(f'{path}/GuardButton.qss') as style:
            self.setStyleSheet(style.read())
            
        self.setIcon(QIcon(img_path))
        self.setIconSize(QSize(20, 20))
        