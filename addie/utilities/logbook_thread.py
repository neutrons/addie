from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import (QThread, Signal)  # noqa
import time


class LogbookThread(QThread):

    last_files = []
    update_text = Signal(str)   # TODO
    refresh_rate_s = 5

    def __init__(self):
        QThread.__init__(self)

    def setup(self, parent=None):
        self.parent = parent

    def run(self):
        while(True):
            self._displaying_log_files()
            time.sleep(self.refresh_rate_s)

    def stop(self):
        self.terminate()

    def _displaying_log_files(self):
        self.update_text.emit('update list')
