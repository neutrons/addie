from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import (QThread)
import os


class RunThread(QThread):

    def setup(self, script=None):
        self.script = script

    def run(self):
        if self.script is None:
            return

        os.system(self.script)
