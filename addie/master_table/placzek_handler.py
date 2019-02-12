from qtpy.QtWidgets import QMainWindow
from addie.utilities import load_ui

# try:
#     from PyQt4.QtGui import QMainWindow
#     from PyQt4 import QtCore, QtGui
# except ImportError:
#     try:
#         from PyQt5.QtWidgets import QMainWindow
#         from PyQt5 import QtCore, QtGui
#     except ImportError:
#         raise ImportError("Requires PyQt4 or PyQt5")

#from addie.ui_placzek import Ui_MainWindow as UiMainWindow


class PlaczekHandler:

    def __init__(self, parent=None, key=None, data_type='sample'):

        if parent.placzek_ui == None:
            parent.placzek_ui = PlaczekWindow(parent=parent, key=key, data_type=data_type)
            parent.placzek_ui.show()
        else:
            parent.placzek_ui.activateWindow()
            parent.placzek_ui.setFocus()

class PlaczekWindow(QMainWindow):

    parent = None
    data_type = None
    key = None

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.data_type = data_type
        self.key = key

        QMainWindow.__init__(self, parent=parent)
        #self.ui = UiMainWindow()
        self.ui = load_ui('ui_placzek.ui', baseinstance=self)
        #self.ui.setupUi(self)

        self.init_widgets()

    def init_widgets(self):
        '''initialize the widgets in the state we left them last time (for the same row)'''
        master_table_list_ui = self.parent.master_table_list_ui[self.key]
        if master_table_list_ui[self.data_type]['placzek_infos'] == None:
            return

        # initialize the widgets using previous values set
        info_dict = master_table_list_ui[self.data_type]['placzek_infos']

        order_index = info_dict['order_index']
        self.ui.order_comboBox.setCurrentIndex(order_index)

        is_self = info_dict['is_self']
        self.ui.self_checkBox.setChecked(is_self)

        is_interference = info_dict['is_interference']
        self.ui.interference_checkBox.setChecked(is_interference)

        fit_spectrum_index = info_dict['fit_spectrum_index']
        self.ui.fit_spectrum_comboBox.setCurrentIndex(fit_spectrum_index)

        lambda_fit_min = str(info_dict['lambda_fit_min'])
        self.ui.lambda_fit_min.setText(lambda_fit_min)

        lambda_fit_max = str(info_dict['lambda_fit_max'])
        self.ui.lambda_fit_max.setText(lambda_fit_max)

        lambda_fit_delta = str(info_dict['lambda_fit_delta'])
        self.ui.lambda_fit_delta.setText(lambda_fit_delta)

        lambda_calc_min = str(info_dict['lambda_calc_min'])
        self.ui.lambda_calc_min.setText(lambda_calc_min)

        lambda_calc_max = str(info_dict['lambda_calc_max'])
        self.ui.lambda_calc_max.setText(lambda_calc_max)

        lambda_calc_delta = str(info_dict['lambda_calc_delta'])
        self.ui.lambda_calc_delta.setText(lambda_calc_delta)

    def save_widgets(self):
        master_table_list_ui = self.parent.master_table_list_ui[self.key]

        order_combobox_text = self.ui.order_comboBox.currentText()
        order_combobox_index = self.ui.order_comboBox.currentIndex()
        is_self_checked = self.ui.self_checkBox.isChecked()
        is_interference_checked = self.ui.interference_checkBox.isChecked()
        fit_spectrum_combobox_text = self.ui.fit_spectrum_comboBox.currentText()
        fit_spectrum_combobox_index = self.ui.fit_spectrum_comboBox.currentIndex()
        lambda_fit_min = self.ui.lambda_fit_min.text()
        lambda_fit_max = self.ui.lambda_fit_max.text()
        lambda_fit_delta = self.ui.lambda_fit_delta.text()
        lambda_calc_min = self.ui.lambda_calc_min.text()
        lambda_calc_max = self.ui.lambda_calc_max.text()
        lambda_calc_delta = self.ui.lambda_calc_delta.text()

        info_dict = {'order_text': order_combobox_text,
                     'order_index': order_combobox_index,
                     'is_self': is_self_checked,
                     'is_interference': is_interference_checked,
                     'fit_spectrum_text': fit_spectrum_combobox_text,
                     'fit_spectrum_index': fit_spectrum_combobox_index,
                     'lambda_fit_min': lambda_fit_min,
                     'lambda_fit_max': lambda_fit_max,
                     'lambda_fit_delta': lambda_fit_delta,
                     'lambda_calc_min': lambda_calc_min,
                     'lambda_calc_max': lambda_calc_max,
                     'lambda_calc_delta': lambda_calc_delta}

        master_table_list_ui[self.data_type]['placzek_infos'] = info_dict
        self.parent.master_table_list_ui[self.key] = master_table_list_ui

    def ok_pressed(self):
        self.save_widgets()
        self.close()

    def cancel_pressed(self):
        self.close()

    def closeEvent(self, c):
        self.parent.placzek_ui = None
