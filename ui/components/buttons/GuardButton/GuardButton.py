from ui.components.buttons.DefaultButton.DefaultButton import DefaultButton


class GuardButton(DefaultButton):
    def __init__(self, state, parent=None):
        self.state = state
        super().__init__(parent)
    
    def setup(self):
        if not self.state:
            self.setObjectName('GuardButtonAdd')
        else:
            self.setObjectName('GuardButtonRemove')
        with open('steam-trade/ui/components/buttons/GuardButton/GuardButton.qss') as style:
            self.setStyleSheet(style.read())