import threading
import types
import inspect


# IPython monkey patches the  pygments.lexer.RegexLexer.get_tokens_unprocessed method
# and breaks Sphinx when running within MantidPlot.
# We store the original method definition here on the pygments module before importing IPython
from pygments.lexer import RegexLexer
# Monkeypatch!
RegexLexer.get_tokens_unprocessed_unpatched = RegexLexer.get_tokens_unprocessed

from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
#from qtconsole.rich_ipython_widget import RichIPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
#import qtconsole.inprocess

from PyQt4 import QtGui


def our_run_code(self, code_obj, result=None):
    """ Method with which we replace the run_code method of IPython's InteractiveShell class.
        It calls the original method (renamed to ipython_run_code) on a separate thread
        so that we can avoid locking up the whole of MantidPlot while a command runs.
        Parameters
        ----------
        code_obj : code object
          A compiled code object, to be executed
        result : ExecutionResult, optional
          An object to store exceptions that occur during execution.
        Returns
        -------
        False : Always, as it doesn't seem to matter.
    """

    t = threading.Thread()
    #ipython 3.0 introduces a third argument named result
    nargs = len(inspect.getargspec(self.ipython_run_code).args)
    if (nargs == 3):
        t = threading.Thread(target=self.ipython_run_code, args=[code_obj,result])
    else:
        t = threading.Thread(target=self.ipython_run_code, args=[code_obj])
    t.start()
    while t.is_alive():
        QtGui.QApplication.processEvents()
    # We don't capture the return value of the ipython_run_code method but as far as I can tell
    #   it doesn't make any difference what's returned
    return 0


class MantidIPythonWidget(RichIPythonWidget):
    """ Extends IPython's qt widget to include setting up and in-process kernel as well as the
        Mantid environment, plus our trick to avoid blocking the event loop while processing commands.
        This widget is set in the QDockWidget that houses the script interpreter within ApplicationWindow.
    """

    def __init__(self, *args, **kw):
        super(MantidIPythonWidget, self).__init__(*args, **kw)

        # Create an in-process kernel
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel = kernel_manager.kernel
        kernel.gui = 'qt4'

        # Figure out the full path to the mantidplotrc.py file and then %run it
        from os import path
        mantidplotpath = path.split(path.dirname(__file__))[0] # It's the directory above this one
        mantidplotrc = path.join(mantidplotpath, 'mantidplotrc.py')
        shell = kernel.shell
        shell.run_line_magic('run', mantidplotrc)
        print '[DB...BAUnderstand]: shell run: ', mantidplotrc

        # These 3 lines replace the run_code method of IPython's InteractiveShell class (of which the
        # shell variable is a derived instance) with our method defined above. The original method
        # is renamed so that we can call it from within the our_run_code method.
        f = shell.run_code
        shell.run_code = types.MethodType(our_run_code, shell)
        shell.ipython_run_code = f

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client

    def write_command(self, command):
        self._store_edits()
        self.input_buffer = command
        return

    def history_previous(self, substring='', as_prefix=True):
        """ If possible, set the input buffer to a previous history item.

            Parameters
            ----------
            substring : str, optional
                If specified, search for an item with this substring.
            as_prefix : bool, optional
                If True, the substring must match at the beginning (default).

            Returns
            -------
            Whether the input buffer was changed.
        """
        print 'Am I here?'
        index = self._history_index
        replace = False
        while index > 0:
                index -= 1
                history = self._get_edited_history(index)
                if (as_prefix and history.startswith(substring)) \
                        or (not as_prefix and substring in history):
                    replace = True
                    break

        if replace:
                self.input_buffer += ' ... da da da'
                self._store_edits()
                self._history_index = index
                self.input_buffer = history + '... da ddd'

        return replace

