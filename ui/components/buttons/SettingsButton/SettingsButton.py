from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class SettingsButton(DefaultButton):
    
    def setup(self):
        self.setObjectName('SettingsButton')
        with open('steam-trade/ui/components/buttons/SettingsButton/SettingsButton.qss') as style:
            self.setStyleSheet(style.read())
