from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from config import (
    PATH_TO_SETTINGS_BUTTON_IMAGE, 
    PATH_TO_SETTINGS_BUTTON_STYLES
)
from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class SettingsButton(DefaultButton):
    
    def setup(self):
        img_path = PATH_TO_SETTINGS_BUTTON_IMAGE
        self.setObjectName('SettingsButton')
        self.setIcon(QIcon(img_path))
        self.setIconSize(QSize(20, 20))
        with open(PATH_TO_SETTINGS_BUTTON_STYLES) as style:
            self.setStyleSheet(style.read())
        