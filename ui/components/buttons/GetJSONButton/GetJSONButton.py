from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GetJSONButton(DefaultButton):
    
    def setup(self):
        path = Path(__file__).parent
        img_path = f'{path.parent.parent.parent}/assets/get_json.png'
        self.setObjectName('GetJSONButton')
        with open(f'{path}/GetJSONButton.qss') as style:
            styles = style.read()
            self.setStyleSheet(styles)
            
        self.setIcon(QIcon(img_path))
        self.setIconSize(QSize(32, 32))
            