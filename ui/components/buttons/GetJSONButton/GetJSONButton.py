from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from config import PATH_TO_GET_JSON_BUTTON_IMAGE, PATH_TO_GET_JSON_BUTTON_STYLES 
from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GetJSONButton(DefaultButton):
    
    def setup(self):
        img_path = PATH_TO_GET_JSON_BUTTON_IMAGE
        self.setObjectName('GetJSONButton')
        self.setIcon(QIcon(img_path))
        self.setIconSize(QSize(32, 32))
        with open(PATH_TO_GET_JSON_BUTTON_STYLES) as style:
            styles = style.read()
            self.setStyleSheet(styles)  
            