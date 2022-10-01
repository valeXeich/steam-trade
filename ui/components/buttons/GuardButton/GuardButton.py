from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GuardButton(DefaultButton):
    
    def setup(self):
        self.setObjectName('GuardButton')
        with open('steam-trade/ui/components/buttons/GuardButton/GuardButton.qss') as style:
            self.setStyleSheet(style.read())