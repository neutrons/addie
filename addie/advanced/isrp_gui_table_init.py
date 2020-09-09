from __future__ import (absolute_import)
from qtpy.QtWidgets import (QMessageBox, QFileDialog)
import os


class IsRepGuiTableInitialization(object):


    def __init__(self, parent=None):
        self.parent = parent
        self.parameters={}

    def _is_table_input_valid(self):
        '''
        Validate the table input
        :return: True if all checks are valid, False otherwise
        :rtype: bool
        '''
        if not self.parent.ui.sample_1_title.text().strip():
            self.err_messenger("'Sample-1 Title' missing!")
            return False

        if not self.parent.ui.sample_2_title.text().strip():
            self.err_messenger("'Sample-1 Title' missing!")
            return False

        if not self.parent.ui.bkg_title.text().strip():
            self.err_messenger("'Background Title' missing!")
            return False

        if not self.parent.ui.bkg_scans.text().strip():
            self.err_messenger("'Background Scans' missing!")
            return False

        if not self.parent.ui.sample_1_scans.text().strip():
            self.err_messenger("'Sample-1 Scans' missing!")
            return False

        if not self.parent.ui.sample_2_scans.text().strip():
            self.err_messenger("'Sample-2 Scans' missing!")
            return False

        if not self.parent.ui.secondary_scattering_ratio.text().strip():
            self.err_messenger("'Secondary Scattering Ratio' missing!")
            return False

        cond1 = self.parent.ui.plazcek_fit_range_min.text().strip()
        cond2 = self.parent.ui.plazcek_fit_range_max.text().strip()
        if not cond1 or not cond2:
            self.err_messenger("Plazcek info incomplete!")
            return False

        cond1 = self.parent.ui.subs_init.text().strip()
        cond2 = self.parent.ui.subs_rep.text().strip()
        if not cond1 or not cond2:
            self.err_messenger("Substitution info incomplete!")
            return False

        cond1 = self.parent.ui.ft_qrange.text().strip()
        cond2 = self.parent.ui.ff_rrange.text().strip()
        cond3 = self.parent.ui.ff_qrange.text().strip()
        if not cond1 or not cond2 or not cond3:
            self.err_messenger("Fourier transform info incomplete!")
            return False

        return True

    def load_fod_input(self):
        _current_folder = self.parent.parent.current_folder
        [_table_file, _] = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption="Input inp File",
            directory=_current_folder,
             filter=("inp files (*.inp);; All Files (*.*)"))

        if not _table_file:
            return

        try:
            fod_inputs = open(_table_file, "r")
        except IOError:
            self.err_messenger("Permission denied! Choose another input file!")
            return

        lines = fod_inputs.readlines()
        fod_inputs.close()

        for line in lines:
            try:
                if line.strip():
                    self.parameters[line.split('#')[1].strip()]=line.split('#')[0].strip()
            except IndexError:
                pass

        try:
            self.parent.ui.sample_1_title.setText(self.parameters['sample_1_title'])
            self.parent.ui.sample_2_title.setText(self.parameters['sample_2_title'])
            self.parent.ui.bkg_title.setText(self.parameters['background_title'])
            self.parent.ui.bkg_scans.setText(self.parameters['background scannrs'])
            self.parent.ui.sample_1_scans.setText(self.parameters['sample_1_scannrs'])
            self.parent.ui.sample_2_scans.setText(self.parameters['sample_2_scannrs'])
            self.parent.ui.secondary_scattering_ratio.setText(self.parameters['secondary_scattering_ratio'])
            self.parent.ui.plazcek_fit_range_min.setText(self.parameters['pla_range'].split(',')[0].strip())
            self.parent.ui.plazcek_fit_range_max.setText(self.parameters['pla_range'].split(',')[1].strip())
            if ',' in self.parameters['substitution_type']:
                self.parent.ui.subs_init.setText(self.parameters['substitution_type'].split(',')[0].strip())
                self.parent.ui.subs_rep.setText(self.parameters['substitution_type'].split(',')[1].strip())
            elif '/' in self.parameters['substitution_type']:
                self.parent.ui.subs_init.setText(self.parameters['substitution_type'].split('/')[0].strip())
                self.parent.ui.subs_rep.setText(self.parameters['substitution_type'].split('/')[1].strip())
            self.parent.ui.ft_qrange.setText(self.parameters['qrangeft'])
            self.parent.ui.ff_rrange.setText(self.parameters['fourier_range_r'])
            try:
                self.parent.ui.ff_qrange.setText(self.parameters['fourier_range_q'])
            except KeyError:
                self.parent.ui.ff_qrange.setText(self.parameters['fourier_range_Q'])

        except (IndexError, KeyError):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Error in FOD input file!")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return

        return

    def err_messenger(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
        return

    def save_fod_input(self):
        valid = self._is_table_input_valid()
        if not valid:
            return

        _current_folder = self.parent.parent.current_folder
        [_out_file, _] = QFileDialog.getSaveFileName(
            parent=self.parent,
            caption="Output inp File",
            directory=_current_folder,
            filter=("inp files (*.inp);; All Files (*.*)"))

        if not _out_file:
            return

        try:
            with open(_out_file, "w") as fod_output:
                self.write_fod_file(fod_output)
        except IOError:
            self.err_messenger("Permission denied! Choose another save target!")
            return
        return

    def save_and_run_fod_input(self):
        valid = self._is_table_input_valid()
        if not valid:
            return

        _current_folder = self.parent.parent.current_folder
        working_dir = QFileDialog.getExistingDirectory(
            self.parent,
            "Select Working Directory",
            _current_folder,
            QFileDialog.ShowDirsOnly)

        if not working_dir:
            return

        out_filename = "fod.inp"
        try:
            with open(os.path.join(working_dir, out_filename), "w") as fod_output:
                self.write_fod_file(fod_output)
        except IOError:
            self.err_messenger("Permission denied! Choose another working folder!")
            return

        os.chdir(working_dir)
        os.system("python /SNS/users/zjn/pytest/FOD.py -f fod.inp")

        return

    def write_fod_file(self, out):
        '''
        Writes FOD file to output file handle
        :param out: File handle
        '''
        out.write(self.parent.ui.sample_1_title.text() + "  # sample_1_title\n")
        out.write(self.parent.ui.sample_2_title.text() + "  # sample_2_title\n")
        out.write(self.parent.ui.bkg_title.text() + "  # background_title\n")
        out.write(self.parent.ui.bkg_scans.text() + "  # background scannrs\n")
        out.write(self.parent.ui.sample_1_scans.text() + "  # sample_1_scannrs\n")
        out.write(self.parent.ui.sample_2_scans.text() + "  # sample_2_scannrs\n")
        out.write(self.parent.ui.subs_init.text() + " / " + self.parent.ui.subs_rep.text() + "  # substitution_type\n")
        out.write(str(self.parent.ui.ndeg.value()) + "  # pla_type\n")
        out.write(self.parent.ui.plazcek_fit_range_min.text() + ", " + self.parent.ui.plazcek_fit_range_max.text() + "  # pla_range\n")
        out.write(self.parent.ui.ft_qrange.text() + "  # qrangeft\n")
        out.write(self.parent.ui.ff_rrange.text() + "  # fourier_range_r\n")
        out.write(self.parent.ui.ff_qrange.text() + "  # fourier_range_Q\n")
        out.write(self.parent.ui.secondary_scattering_ratio.text() + "  # secondary_scattering_ratio")
        return

    def iso_rep_linker(self):
        self.parent.ui.load_fod_input_button.clicked.connect(self.load_fod_input)
        self.parent.ui.save_fod_input_button.clicked.connect(self.save_fod_input)
        self.parent.ui.save_and_run_fod_input.clicked.connect(self.save_and_run_fod_input)
        return

