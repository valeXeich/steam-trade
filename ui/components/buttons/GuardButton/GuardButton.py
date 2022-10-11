from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from config import (
    PATH_TO_GUARD_ADD_BUTTON_IMAGE, 
    PATH_TO_GUARD_REMOVE_BUTTON_IMAGE, 
    PATH_TO_GUARD_BUTTON_STYLES
)
from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GuardButton(DefaultButton):
    def __init__(self, state, parent=None):
        self.state = state
        super().__init__(parent)
    
    def setup(self):
        self.setObjectName('GuardButton')
        if not self.state:
            img_path = PATH_TO_GUARD_ADD_BUTTON_IMAGE
        else:
            img_path = PATH_TO_GUARD_REMOVE_BUTTON_IMAGE
        self.setIcon(QIcon(img_path))
        self.setIconSize(QSize(20, 20))
        
        with open(PATH_TO_GUARD_BUTTON_STYLES) as style:
            self.setStyleSheet(style.read())
        