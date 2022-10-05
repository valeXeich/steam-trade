from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class SettingsButton(DefaultButton):
    
    def setup(self):
        path = Path(__file__).parent
        img_path = f'{path.parent.parent.parent}/assets/settings.png'
        self.setObjectName('SettingsButton')
        with open(f'{path}/SettingsButton.qss') as style:
            self.setStyleSheet(style.read())

        self.setIcon(QIcon(img_path))
        self.setIconSize(QSize(20, 20))
        