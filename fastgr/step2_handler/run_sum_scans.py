import os
from PyQt4.QtCore import Qt


class RunSumScans(object):
    
    script = 'python  /SNS/users/zjn/pytest/sumscans.py '
    output_file = ''
    
    def __init__(self, parent=None):
        self.parent = parent.ui
        self.parent_no_ui = parent
        self.folder = os.getcwd()
        
    def run(self):
        self._background = self.collect_background_runs()
        self._runs = self.collect_runs_checked()
        self.create_output_file()
        self.run_script()

    def run_script(self):
        _script_to_run = self.add_script_flags()
        _script_to_run += ' -f ' + self.full_output_file_name + ' &'

        _run_thread = self.parent_no_ui._run_thread_sum_scans
        _run_thread.setup(script = _script_to_run)
        _run_thread.start()
        
#        os.system(_script_to_run)
        print("[LOG] executing in its own thread:")
        print("[LOG] " + _script_to_run)
        
    def add_script_flags(self):
        _script = self.script

        if not self.parent.interactive_mode_checkbox.isChecked():
            _script +=  "-n True"
            
        qmax_list = str(self.parent.pdf_qmax_line_edit.text()).strip()
        if not (qmax_list  == ""):
            _script  += ' -q ' + qmax_list

        return _script

    def create_output_file(self):
        _output_file_name = "sum_" + self.parent.sum_scans_output_file_name.text() + ".inp"
        print("_output_file_name: {}".format(_output_file_name))
        _full_output_file_name = os.path.join(self.folder, _output_file_name)
        print("_full_output_file_name: {}".format(_full_output_file_name))
        self.full_output_file_name = _full_output_file_name
        
        f = open(_full_output_file_name, 'w')
        
        f.write("background %s\n" %self._background)
        for _label in self._runs.keys():
            f.write("%s %s\n" %(_label, self._runs[_label]))
            
        f.close()
        print("[LOG] created file %s" %_full_output_file_name)
        
    def collect_runs_checked(self):
        _runs = {}
        for _row_index in range(self.parent.table.rowCount()):
            _selected_widget = self.parent.table.cellWidget(_row_index, 0).children()[1]
            if (_selected_widget.checkState() == Qt.Checked):
                _label = str(self.parent.table.item(_row_index, 1).text())
                _value = str(self.parent.table.item(_row_index, 2).text())
                _runs[_label] = _value
                
        return _runs

    def collect_background_runs(self):
        if self.parent.background_no.isChecked():
            _background = str(self.parent.background_no_field.text())
        else:
            _background = str(self.parent.background_line_edit.text())
        return _background
        