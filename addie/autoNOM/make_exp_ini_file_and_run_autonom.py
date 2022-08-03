from __future__ import (absolute_import, division, print_function)
import os
import time
import simplejson
from datetime import datetime
import re

from addie.autoNOM.step1_gui_handler import Step1GuiHandler


class MakeExpIniFileAndRunAutonom(object):

    _dict_mandatory = None
    _dict_optional = None
    EXP_INI_FILENAME = 'exp.ini'
    _star = '*' * 19
    title_mandatory = 'required ' + _star
    _star = '*' * 18
    title_optional = 'optional ' + _star
    list_mandatory = ['Dia', 'DiaBg', 'Vana', 'VanaBg', 'MTc']
    list_optional = ['recali', 'renorm', 'autotemp', 'scan1', 'scanl', 'Hz', '#']
    script_to_run = "/usr/bin/python /SNS/NOM/shared/autoNOM/stable/autoNOM.py -l -P /SNS/NOM/shared/autoNOM/stable/"
    script_flag = ""

    def __init__(self, parent=None, folder=None):
        self.parent_no_ui = parent
        # self.parent = parent.ui
        self.parent = parent.autonom_ui
        self.folder = folder
        self.script_to_run = "/usr/bin/python " + parent._autonom_script + " -l -P " + parent.idl_script_dir

    def create(self):
        self.retrieve_metadata()
        self.create_exp_ini_file()

    def retrieve_flags(self):
        _postprocessing_flag = self.parent.postprocessing_yes.isChecked()
        self.script_flag += " -p %s" % _postprocessing_flag

    def run_autonom(self):
        self.retrieve_flags()
        self.run_auto_nom_script()

    def retrieve_metadata(self):
        _dict_mandatory = {}
        _dict_optional = {}

        _diamond = str(self.parent.diamond.text())
        _diamond_background = str(self.parent.diamond_background.text())
        _vanadium = str(self.parent.vanadium.text())
        _vanadium_background = str(self.parent.vanadium_background.text())
        _sample_background = str(self.parent.sample_background.text())

        _first_scan = str(self.parent.first_scan.text())
        _last_scan = str(self.parent.last_scan.text())
        _frequency = self.parent.frequency.currentText()

        _recalibration_flag = self.yes_no(self.parent.recalibration_yes.isChecked())
        _renormalization_flag = self.yes_no(self.parent.renormalization_yes.isChecked())
        _autotemplate_flag = self.yes_no(self.parent.autotemplate_yes.isChecked())

        _comments = self.parent.comments.text()

        _dict_mandatory['Dia'] = _diamond
        _dict_mandatory['DiaBg'] = _diamond_background
        _dict_mandatory['Vana'] = _vanadium
        _dict_mandatory['VanaBg'] = _vanadium_background
        _dict_mandatory['MTc'] = _sample_background
        _dict_optional['recali'] = _recalibration_flag
        _dict_optional['renorm'] = _renormalization_flag
        _dict_optional['autotemp'] = _autotemplate_flag
        _dict_optional['scan1'] = _first_scan
        _dict_optional['scanl'] = _last_scan
        _dict_optional['Hz'] = _frequency
        _dict_optional['#'] = _comments

        self._dict_mandatory = _dict_mandatory
        self._dict_optional = _dict_optional

    def get_previous_cycle_cal_path(cycle, year, calstring="/SNS/NOM/shared/CALIBRATION/%s_%d_1B_CAL/"):
        if cycle == 1:
            _old_year = int(year) - 1
            _calpath = calstring % (_old_year, 2)
        else:
            _calpath = calstring % (year, 1)

        return _calpath

    def check_calfiles_in_calpath(calpath, calibrant, samp_env, same_samp_env_dict=None, file_extension='.h5'):

        cal_list = [os.path.splitext(filename) for filename in os.listdir(calpath)]

        if same_samp_env_dict is None:
            same_samp_env_dict = dict()

        found_in_cycle = False
        cal_file = None
        for basename, ext in cal_list:
            if file_extension in ext:
                _pulled_run = re.search(r'd(\d+)', basename.split('_')[1]).group(1)  # parses "d####" str for number
                _pulled_samp_env = basename.split('_')[-1]

                _full_path = calpath+basename+ext

                if _pulled_run == calibrant and _pulled_samp_env == samp_env:
                    found_in_cycle = True
                    cal_file = _full_path

                if _pulled_run != calibrant and _pulled_samp_env == samp_env:
                    same_samp_env_dict[int(_pulled_run)] = _full_path

        return found_in_cycle, same_samp_env_dict, cal_file

    def setup_mantid_calibration(self, script='calibration_creation.py',
                                 input_file='calibration_creation.json',
                                 script_dir='/SNS/NOM/shared/scripts/',
                                 calstring="/SNS/NOM/shared/CALIBRATION/%s_%d_1B_CAL/",
                                 calformat="NOM_d%d_%s_%s.h5"):

        # Setup calibration input
        _diamond = self._dict_mandatory['Dia']
        _vanadium = self._dict_mandatory['Vana']
        _today = datetime.now().date().strftime("%Y_%m_%d")
        _samp_env = str(self.parent.sample_environment_comboBox.currentText())

        _script_to_run = script_dir+script+' '+input_file

        # Get cycle based on month and year
        _year = datetime.now().date().strftime("%Y")
        _month = datetime.now().date().strftime("%m")
        if int(_month) <= 6:
            _cycle = 1
        else:
            _cycle = 2
        _calpath = calstring % (_year, _cycle)

        # Check current cycle directory exists and make if not
        if not os.path.isdir(_calpath):
            os.mkdir(_calpath)

        # Check current cycle for calibration
        found_in_current_cycle, same_sample_env_dict, current_cal_file = \
            self.check_calfiles_in_calpath(calpath=_calpath, calibrant=_diamond,
                                           samp_env=_samp_env, same_samp_env_dict=None,
                                           file_extention='.h5')

        # Check previous cycle for calibration
        _calpath = self.get_previous_cycle_cal_path(_cycle, _year)
        found_in_previous_cycle, same_sample_env_dict, old_cal_file = \
            self.check_calfiles_in_calpath(calpath=_calpath, calibrant=_diamond,
                                           samp_env=_samp_env, same_samp_env_dict=same_sample_env_dict,
                                           file_extention='.h5')
        # Get old calibration to use
        old_cal = None
        if same_sample_env_dict:
            old_cal = sorted(same_sample_env_dict)[-1]

        # Finish setting up calibation input
        _cal_input = {"sample": _diamond,
                      "vanadium": _vanadium,
                      "date": _today,
                      "sample_environment": _samp_env,
                      "oldCal": old_cal
                      }

        # Write file if we either did not find a calibration or force rerunning the calibration
        _run_cali = False

        _recalibration_flag = self.parent.recalibration_yes.isChecked()
        if (not found_in_current_cycle and not found_in_previous_cycle) or _recalibration_flag:
            _run_cali = True
            _mantid_calibration = calstring % (_year, _month)
            _mantid_calibration += calformat % (int(_diamond), _today, _samp_env)
            with open(input_file, 'w') as handle:
                simplejson.dump(_cal_input, handle, indent=2, ignore_nan=True)
        elif not found_in_current_cycle and found_in_previous_cycle:
            _mantid_calibration = current_cal_file
        elif found_in_previous_cycle:
            _mantid_calibration = old_cal_file

        return _run_cali, _mantid_calibration, _script_to_run

    def create_exp_ini_file(self):

        _full_file_name = os.path.join(self.folder, self.EXP_INI_FILENAME)

        f = open(_full_file_name, 'w')

        # mandatory part
        _dict_mandatory = self._dict_mandatory
        f.write(self.title_mandatory + "\n")
        for _name in self.list_mandatory:
            f.write(_name + ' ' + _dict_mandatory[_name] + '\n')

        # optional part
        _dict_optional = self._dict_optional
        f.write(self.title_optional + '\n')
        for _name in self.list_optional:
            _value = _dict_optional[_name]
            if _value == '':
                continue
            else:
                f.write(_name + ' ' + _dict_optional[_name] + '\n')

        f.close()
        print("[LOG] created file %s" % _full_file_name)

    def run_auto_nom_script(self):
        _script_to_run = self.script_to_run + self.script_flag
        os.chdir(self.folder)

        print("[LOG] " + _script_to_run)
        # o_gui = Step1GuiHandler(parent=self.parent_no_ui)
        o_gui = Step1GuiHandler(main_window=self.parent_no_ui)
        o_gui.set_main_window_title()

        _dict_mandatory = self._dict_mandatory
        _pre_script = '/usr/bin/python /SNS/NOM/shared/autoNOM/stable/readtitles.py -a -s'
        for _values in list(_dict_mandatory.values()):
            _pre_script += ' ' + _values

        '''
        print("[LOG] testing Mantid calibration")
        _run_cali, _mantid_calibration, _script_to_run = self.setup_mantid_calibration()
        if _run_cali:
            self.parent_no_ui.launch_job_manager(job_name = 'Mantid calibration',
                                                 script_to_run = _script_to_run)
        '''

        print("[LOG] running pre-script")
        print("[LOG] " + _pre_script)
        os.system(_pre_script)

        while not os.path.isfile("./los.txt"):
            time.sleep(1)

        print("[LOG] running script:")
        print("[LOG] " + _script_to_run)
        self.parent_no_ui.launch_job_manager(job_name='autoNOM',
                                             script_to_run=_script_to_run)

#        os.system(_script_to_run)
#        self.parent.statusbar.showMessage("autoNOM script: DONE !")

    def yes_no(self, condition):
        if condition:
            return "yes"
        else:
            return "no"
