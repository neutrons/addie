from __future__ import (absolute_import, division, print_function)
import os
from addie.utilities.file_handler import FileHandler
from addie.autoNOM.step1_widgets_handler import Step1WidgetsHandler


class AutoPopulateWidgets(object):

    input_file_name = 'exp.ini'
    file_found_message = "Config file %s has been found!" % input_file_name
    file_not_found_message = "Config file %s has  not been found! " % input_file_name

    def __init__(self, main_window=None):
        self.main_window = main_window
#        self.main_window.autonom_ui = parent.ui

    def run(self):
        full_file_name = os.path.join(self.main_window.current_folder, self.input_file_name)
        if os.path.exists(full_file_name):
            self.main_window.autonom_ui.exp_ini_file_status.setText(self.file_found_message)
            o_retriever = RetrieveExpIniConfiguration(exp_ini_file_name=full_file_name)
            o_retriever.run()
            self.populate_widgets(o_retriever.exp_ini_dico)
            return

        self.main_window.autonom_ui.exp_ini_file_status.setText(self.file_not_found_message)

    def populate_widgets(self, widgets_dico):
        self.main_window.autonom_ui.diamond.setText(widgets_dico['Dia'])
        self.main_window.autonom_ui.diamond_background.setText(widgets_dico['DiaBg'])
        self.main_window.autonom_ui.vanadium.setText(widgets_dico['Vana'])
        self.main_window.autonom_ui.vanadium_background.setText(widgets_dico['VanaBg'])
        self.main_window.autonom_ui.sample_background.setText(widgets_dico['MTc'])

        o_gui = Step1WidgetsHandler(parent=self.main_window)

        try:
            _recali = True if (widgets_dico['recali'].strip() == 'yes') else False
        except:
            _recali = False
        finally:
            o_gui.set_recalibration(_recali)

        try:
            _renorm = True if (widgets_dico['renorm'].strip() == 'yes') else False
        except:
            _renorm = False
        finally:
            o_gui.set_renormalization(_renorm)

        try:
            _auto = True if (widgets_dico['autotemp'].strip() == 'yes') else False
        except:
            _auto = False
        finally:
            o_gui.set_autotemplate(_auto)

        self.main_window.autonom_ui.first_scan.setText(widgets_dico['scan1'])
        self.main_window.autonom_ui.last_scan.setText(widgets_dico['scanl'])

        if str(self.main_window.autonom_ui.frequency.currentText()) == '60':
            self.main_window.autonom_ui.frequency.setCurrentIndex(0)
        else:
            self.main_window.autonom_ui.frequency.setCurrentIndex(1)

        try:
            _comments = widgets_dico['#']
        except:
            _comments = ''
        finally:
            self.main_window.autonom_ui.comments.setText(_comments)


class RetrieveExpIniConfiguration(object):

    exp_ini_dico = {}

    def __init__(self, exp_ini_file_name=None):
        self.full_file_name = exp_ini_file_name

    def run(self):
        o_file = FileHandler(filename=self.full_file_name)
        o_file.retrieve_contain()
        _file_contrain = o_file.file_contain

        self.retrieve_settings(_file_contrain)

    def retrieve_settings(self, file_contain):
        _exp_ini_dico = {}
        file_contain = file_contain.split("\n")
        for _line in file_contain:
            _parsed_line = _line.split()
            if len(_parsed_line) > 1:
                _keyword = _parsed_line[0]
                if _keyword == '#':
                    _value = " ".join(_parsed_line[1:])
                else:
                    _value = _parsed_line[1]
                _exp_ini_dico[_keyword] = _value

        self.exp_ini_dico = _exp_ini_dico
