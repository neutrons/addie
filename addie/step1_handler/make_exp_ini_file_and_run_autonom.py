import os
import time
import json
from datetime import datetime

from addie.step1_handler.step1_gui_handler import Step1GuiHandler


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
    script_to_run = "python /SNS/NOM/shared/autoNOM/stable/autoNOM.py -l -P /SNS/NOM/shared/autoNOM/stable/"
    script_flag = ""
    
    def __init__(self, parent=None, folder=None):
        self.parent_no_ui = parent
        self.parent = parent.ui
        self.folder = folder
        
    def create(self):
        self.retrieve_metadata()
        self.create_exp_ini_file()
        
    def retrieve_flags(self):
        _postprocessing_flag = self.parent.postprocessing_yes.isChecked()
        self.script_flag += " -p %s" %_postprocessing_flag

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
       
    def launch_mantid_calibration(self):
        _year=datetime.now().date().strftime("%Y")
        _month=datetime.now().date().strftime("%m")
        if int(_month) <= 6:
            _cycle = 1
        else:
            _cycle = 2
        _calpath="/SNS/NOM/shared/CALIBRATION/%s_%d_1B_CAL/" % (_year,_cycle)

        _samp_env = str(self.parent.sample_environment_comboBox.currentText())
        _diamond = self._dict_mandatory['Dia'] 

        found=False
        old_found=False
        cal_list = [ os.path.splitext(filename) for filename in os.listdir(_calpath) ]
        for basename, file_extension in cal_list:
            if '.h5' in file_extension:
                _pulled_run = basename.split('_')[1]
                _pulled_samp_env = basename.split('_')[-1]

                old_found=True
                old_cal = _calpath+"/"+basename+file_extension
                if _pulled_run == 'd'+_diamond and _pulled_samp_env == _samp_env:
                    found = True


        if not found:
            if not old_found:
                if _cycle == 1:
                    _old_year = int(year) - 1
                    _calpath="/SNS/NOM/shared/CALIBRATION/%s_%d_1B_CAL/" % (_old_year,2)
                else:
                    _calpath="/SNS/NOM/shared/CALIBRATION/%s_%d_1B_CAL/" % (_year,)
                
            _today=datetime.now().date().strftime("%Y_%m_%d")
            _vanadium = self._dict_mandatory['Vana'] 
            _cal_input = { "sample": _diamond,
                          "vanadium": _vanadium,
                          "date": _today,
                          "sample_environment": _samp_env,
                          "oldCal": old_cal
                        }
    
            with open("calibration_creation.json",'w') as handle:
                json.dump(_cal_input, handle)
            _script_to_run = "/SNS/NOM/shared/scripts/calibration_creation.py calibration_creation.json"
            os.system(_script_to_run)
            
                
        
        print _month, _year, _samp_env, _calpath
 
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
        print("[LOG] created file %s" %_full_file_name)
        
    def run_auto_nom_script(self):
        _script_to_run = self.script_to_run + self.script_flag
        os.chdir(self.folder)
        
        o_gui = Step1GuiHandler(parent = self.parent_no_ui)
        o_gui.set_main_window_title()
        
        _dict_mandatory = self._dict_mandatory
        _pre_script = '/SNS/NOM/shared/autoNOM/stable/readtitles.py -a -s'
        for _values in _dict_mandatory.values():
            _pre_script += ' ' + _values

        print("[LOG] testing Mantid calibration")
        self.launch_mantid_calibration()
        exit()

        print("[LOG] running pre-script")
        print("[LOG] " + _pre_script)
        os.system(_pre_script)
        
        while not os.path.isfile("./los.txt"):
            time.sleep(1)
        
        print("[LOG] running script:")
        print("[LOG] " + _script_to_run)
        self.parent_no_ui.launch_job_manager(job_name = 'autoNOM',
                                             script_to_run = _script_to_run)

#        os.system(_script_to_run)
#        self.parent.statusbar.showMessage("autoNOM script: DONE !")        

    def yes_no(self, condition):
        if condition:
            return "yes"
        else:
            return "no"
