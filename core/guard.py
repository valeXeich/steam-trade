import time

from PyQt5.QtCore import QThread, pyqtSignal


class SteamGuardTimer(QThread):
    counter = pyqtSignal(int)
    
    def __init__(self, guard):
        super().__init__()
        self.guard = guard
    
    def run(self):
        start = self.start_value
        while True:
            start -= 1
            time.sleep(1)
            self.counter.emit(start)
            if start == 0:
                start = 30
    
    @property
    def start_value(self):
        timestamp = self.guard._get_time()
        return 30 - timestamp % 60 % 30
    