import mantid_ipython_widget
import PyQt4.QtGui


class IPythonDockWidget(PyQt4.QtGui.QDockWidget):
    """
    """
    def __init__(self, parent):
        """
        """
        PyQt4.QtGui.QDockWidget.__init__(self, parent)

        self.iPythonWidget = None

        return

    def setup(self):
        """
        """
        # set ipython
        self.iPythonWidget = mantid_ipython_widget.MantidIPythonWidget()
        self.setWidget(self.iPythonWidget)

        return

    def wild_test(self):
        """
        WILD TEST
        Returns
        -------

        """
        # append output to the output stream but not input console
        self.iPythonWidget.append_stream('bababa (append_stream)')

        import os
        file_name = os.path.join(os.getcwd(), 'blabla.py')
        self.iPythonWidget.execute_file(file_name)
        # result:
        # %run /home/wzz/Projects/FastGR/test_data/blabla.py
        # Hello World!

        self.iPythonWidget.input_buffer = 'print (nothing)'

        return
        # append to output
        self.iPythonWidget._append_plain_text('22222')

        # not inherit from HistoryConsoleWidget
        # pre_hist = self.iPythonWidget.history_previous()
        # print 'pre_hist = ', pre_hist

        command = 'ws = mtd[abc]'
        self.iPythonWidget.write_command(command)

        return