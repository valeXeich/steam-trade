from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GetJSONButton(DefaultButton):
    
    def setup(self):
        self.setObjectName('GetJSONButton')
        with open('steam-trade/ui/components/buttons/GetJSONButton/GetJSONButton.qss') as style:
            self.setStyleSheet(style.read())
            