from __future__ import (absolute_import, division, print_function)
import numpy as np
import re
import sys
import copy
from periodictable import formula
from qtpy.QtWidgets import QMainWindow, QApplication
from addie.utilities import load_ui
from qtpy import QtGui

from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.processing.mantid.master_table.periodic_table.isotopes_handler import IsotopesHandler
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA


def get_periodictable_formatted_element_and_number_of_atoms(element):
    '''The goal of this method is to go from Mantid format of an element (Si28)2 to
    the format accepted by the periodictable library (to calculate the molecular mass for example) (Si[28]2)'''

    # if we have a single stable element
    regular_expression_1 = r'^(?P<stable_element>[(]{0,1}[A-Z]{1}[a-z]{0,1}[)]{0,1}$)'
    m1 = re.search(regular_expression_1, element)
    if m1 is not None:
        case = 1
        return [m1.group('stable_element'), 1., case]

    # stable with stochiometric coefficient
    regular_expression_2 = r'^(?P<stable_element>[(]{1}[A-Z]{1}[a-z]{0,1}[)]{1})(?P<stochiometric_coefficient>\d*\.{0,1}\d*)$'
    m2 = re.search(regular_expression_2, element)
    if m2 is not None:
        case = 2
        return ["{}{}".format(m2.group('stable_element'), m2.group('stochiometric_coefficient')),
                np.float(m2.group('stochiometric_coefficient')), case]

    # isotope with or without stochiometric coefficient
    regular_expression_3 = r'\((?P<isotope_element>[A-Z]{1}[a-z]{0,1})(?P<isotope_number>\d+)\)' \
                           r'(?P<stochiometric_coefficient>\d*\.{0,1}\d*)'
    m3 = re.search(regular_expression_3, element)
    if m3 is not None:
        case = 3
        if m3.group('stochiometric_coefficient') == "":
            number_of_atoms = 1.
        else:
            number_of_atoms = np.float(
                m3.group('stochiometric_coefficient'))
        return ["{}[{}]{}".format(m3.group('isotope_element'), m3.group('isotope_number'),
                                  m3.group('stochiometric_coefficient')), number_of_atoms, case]

    raise ValueError


def retrieving_molecular_mass_and_number_of_atoms_worked(chemical_formula):
    '''this method will parse the formula to go from Mantid format to periodictable library format, in order
    to calculate the molecular mass

    return: True if the string has been correctly formatted
    False if something went wrong

    '''
    list_element = chemical_formula.split(" ")
    periodictable_list_element_format = []
    total_number_of_atoms = 0.
    try:
        for _element in list_element:
            [formated_element, number_of_atoms, case] = get_periodictable_formatted_element_and_number_of_atoms(
                 _element)
            periodictable_list_element_format.append(formated_element)
            total_number_of_atoms += number_of_atoms

        periodictable_format = " ".join(periodictable_list_element_format)
        periodictable_formula = formula(periodictable_format)
        return periodictable_formula.mass, total_number_of_atoms

    except:
        return None, None


class MaterialHandler:
    def __init__(self, parent=None, database_window=None, key=None, data_type='sample'):
        if parent.material_ui is None:
            o_material = PeriodicTable(parent=parent,
                                       database_window=database_window,
                                       key=key,
                                       data_type=data_type)
            o_material.show()
            parent.material_ui = o_material
            if parent.material_ui_position:
                parent.material_ui.move(parent.material_ui_position)
        else:
            parent.material_ui.setFocus()
            parent.material_ui.activateWindow()


class PeriodicTable(QMainWindow):

    isotope_ui = None
    list_ui_color = {'list_ui': None,
                     'color': None}

    list_color = {0: copy.deepcopy(list_ui_color),
                  1: copy.deepcopy(list_ui_color),
                  2: copy.deepcopy(list_ui_color),
                  3: copy.deepcopy(list_ui_color),
                  4: copy.deepcopy(list_ui_color),
                  5: copy.deepcopy(list_ui_color),
                  6: copy.deepcopy(list_ui_color),
                  7: copy.deepcopy(list_ui_color),
                  }
    column = 0

    def __init__(self, parent=None, database_window=None, key=None, data_type='sample'):

        self.parent = parent
        self.database_window = database_window
        self.key = key
        self.data_type = data_type

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('periodic_table.ui', baseinstance=self)
        self.setWindowTitle("Define Chemical Formula")

        self.init_ui_color_dictionary()
        self.init_widgets()
        self.set_column_index()

    def set_column_index(self):
        if self.data_type == 'sample':
            self.column = INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA[0]
        else:
            self.column = INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA[1]

    def init_ui_color_dictionary(self):

        # color of element buttons

        # purple
        self.list_color[0]['list_ui'] = [self.ui.h,
                                         self.ui.c,
                                         self.ui.n,
                                         self.ui.o,
                                         self.ui.p,
                                         self.ui.s,
                                         self.ui.se,
                                         ]
        self.list_color[0]['color'] = "#938ac0"

        # cyan
        self.list_color[1]['list_ui'] = [self.ui.li,
                                         self.ui.na,
                                         self.ui.k,
                                         self.ui.rb,
                                         self.ui.cs,
                                         self.ui.fr,
                                         ]
        self.list_color[1]['color'] = "#99d5c2"

        # light green
        self.list_color[2]['list_ui'] = [self.ui.be,
                                         self.ui.mg,
                                         self.ui.ca,
                                         self.ui.sr,
                                         self.ui.ba,
                                         self.ui.ra,
                                         ]
        self.list_color[2]['color'] = "#c6e8c1"

        # light yellow
        self.list_color[3]['list_ui'] = [self.ui.b,
                                         self.ui.si,
                                         self.ui.ge,
                                         self.ui.arsenic,
                                         self.ui.sb,
                                         self.ui.te,
                                         self.ui.po,
                                         ]
        self.list_color[3]['color'] = "#eef8b9"

        # dark yellow
        self.list_color[4]['list_ui'] = [self.ui.f,
                                         self.ui.cl,
                                         self.ui.br,
                                         self.ui.i,
                                         self.ui.at,
                                         self.ui.ts,
                                         ]
        self.list_color[4]['color'] = "#fee9b0"

        # blue
        self.list_color[5]['list_ui'] = [self.ui.he,
                                         self.ui.ne,
                                         self.ui.ar,
                                         self.ui.kr,
                                         self.ui.xe,
                                         self.ui.rn,
                                         self.ui.og,
                                         ]
        self.list_color[5]['color'] = "#79afd1"

        # light orange
        self.list_color[6]['list_ui'] = [self.ui.al,
                                         self.ui.ga,
                                         self.ui.indium,
                                         self.ui.sn,
                                         self.ui.tl,
                                         self.ui.pb,
                                         self.ui.bi,
                                         self.ui.nh,
                                         self.ui.fl,
                                         self.ui.mc,
                                         self.ui.lv,
                                         ]
        self.list_color[6]['color'] = "#fec796"

        # dark orange
        self.list_color[7]['list_ui'] = [self.ui.sc,
                                         self.ui.ti,
                                         self.ui.v,
                                         self.ui.cr,
                                         self.ui.mn,
                                         self.ui.fe,
                                         self.ui.co,
                                         self.ui.ni,
                                         self.ui.cu,
                                         self.ui.zn,
                                         self.ui.y,
                                         self.ui.zr,
                                         self.ui.nb,
                                         self.ui.mo,
                                         self.ui.tc,
                                         self.ui.ru,
                                         self.ui.rh,
                                         self.ui.pd,
                                         self.ui.ag,
                                         self.ui.cd,
                                         self.ui.lu,
                                         self.ui.hf,
                                         self.ui.ta,
                                         self.ui.w,
                                         self.ui.re,
                                         self.ui.os,
                                         self.ui.ir,
                                         self.ui.pt,
                                         self.ui.au,
                                         self.ui.hg,
                                         self.ui.lr,
                                         self.ui.rf,
                                         self.ui.db,
                                         self.ui.sg,
                                         self.ui.bh,
                                         self.ui.hs,
                                         self.ui.mt,
                                         self.ui.ds,
                                         self.ui.rg,
                                         self.ui.cn,
                                         ]
        self.list_color[7]['color'] = "#f79d83"

    def init_widgets(self):

        self.ui.save_button.setEnabled(False)

        # init contain of chemical formula
        if self.data_type == 'database':
            # retrieve value from import_from_database label
            text = str(
                self.database_window.list_ui[self.key]['value_label'].text())
        else:
            # retrieve value from sample or normalization columns in master table
            text = str(
                self.parent.master_table_list_ui[self.key][self.data_type]['material']['text'].text())
        if text == 'N/A':
            text = ""
        self.ui.chemical_formula.setText(text)

        # set color of buttons
        for _key in self.list_color.keys():
            _list_ui = self.list_color[_key]['list_ui']
            _color = self.list_color[_key]['color']
            for _ui in _list_ui:
                _ui.setStyleSheet("background-color:{}".format(_color))

        # clear button icon
        self.ui.clear_button.setIcon(
            QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))

    def reset_text_field(self):
        self.ui.chemical_formula.setText("")

    def chemical_formula_changed(self, new_formula):
        self.check_status_save_button()

    def add_new_entry(self, isotope='', number=1, is_natural_element=False):
        if isotope == '':
            return

        previous_chemical_formula = str(self.ui.chemical_formula.text())
        if is_natural_element:
            if number == 1:
                number = ''
            new_isotope_string = "({}){}".format(isotope, number)
        elif number > 1:
            new_isotope_string = "({}){}".format(isotope, number)
        else:
            new_isotope_string = "({})".format(isotope)

        if previous_chemical_formula != '':
            new_chemical_formula = previous_chemical_formula + ' ' + new_isotope_string
        else:
            new_chemical_formula = new_isotope_string

        self.ui.chemical_formula.setText(new_chemical_formula)
        self.ui.chemical_formula.setFocus()

        # make chemical formula editable (bug in pyqt that sometimes turn off editable)

    def click_button(self, element):
        IsotopesHandler(parent=self, element=element.title())

    def h_button(self):
        self.click_button('h')

    def li_button(self):
        self.click_button('li')

    def he_button(self):
        self.click_button('he')

    def be_button(self):
        self.click_button('be')

    def b_button(self):
        self.click_button('b')

    def c_button(self):
        self.click_button('c')

    def n_button(self):
        self.click_button('n')

    def o_button(self):
        self.click_button('o')

    def f_button(self):
        self.click_button('f')

    def ne_button(self):
        self.click_button('ne')

    def na_button(self):
        self.click_button('na')

    def mg_button(self):
        self.click_button('mg')

    def al_button(self):
        self.click_button('al')

    def si_button(self):
        self.click_button('si')

    def p_button(self):
        self.click_button('p')

    def s_button(self):
        self.click_button('s')

    def cl_button(self):
        self.click_button('cl')

    def ar_button(self):
        self.click_button('ar')

    def k_button(self):
        self.click_button('k')

    def ca_button(self):
        self.click_button('ca')

    def sc_button(self):
        self.click_button('sc')

    def ti_button(self):
        self.click_button('ti')

    def v_button(self):
        self.click_button('v')

    def cr_button(self):
        self.click_button('cr')

    def mn_button(self):
        self.click_button('mn')

    def fe_button(self):
        self.click_button('fe')

    def co_button(self):
        self.click_button('co')

    def ni_button(self):
        self.click_button('ni')

    def cu_button(self):
        self.click_button('cu')

    def zn_button(self):
        self.click_button('zn')

    def ga_button(self):
        self.click_button('ga')

    def ge_button(self):
        self.click_button('ge')

    def as_button(self):
        self.click_button('as')

    def se_button(self):
        self.click_button('se')

    def br_button(self):
        self.click_button('br')

    def kr_button(self):
        self.click_button('kr')

    def rb_button(self):
        self.click_button('rb')

    def sr_button(self):
        self.click_button('sr')

    def y_button(self):
        self.click_button('y')

    def zr_button(self):
        self.click_button('zr')

    def nb_button(self):
        self.click_button('nb')

    def mo_button(self):
        self.click_button('mo')

    def tc_button(self):
        self.click_button('tc')

    def ru_button(self):
        self.click_button('ru')

    def rh_button(self):
        self.click_button('rh')

    def pd_button(self):
        self.click_button('pd')

    def ag_button(self):
        self.click_button('ag')

    def cd_button(self):
        self.click_button('cd')

    def in_button(self):
        self.click_button('in')

    def sn_button(self):
        self.click_button('sn')

    def sb_button(self):
        self.click_button('sb')

    def te_button(self):
        self.click_button('te')

    def i_button(self):
        self.click_button('i')

    def xe_button(self):
        self.click_button('xe')

    def cs_button(self):
        self.click_button('cs')

    def ba_button(self):
        self.click_button('ba')

    def lu_button(self):
        self.click_button('lu')

    def hf_button(self):
        self.click_button('hf')

    def ta_button(self):
        self.click_button('ta')

    def w_button(self):
        self.click_button('w')

    def re_button(self):
        self.click_button('re')

    def os_button(self):
        self.click_button('os')

    def ir_button(self):
        self.click_button('ir')

    def pt_button(self):
        self.click_button('pt')

    def au_button(self):
        self.click_button('au')

    def hg_button(self):
        self.click_button('hg')

    def tl_button(self):
        self.click_button('tl')

    def pb_button(self):
        self.click_button('pb')

    def bi_button(self):
        self.click_button('bi')

    def po_button(self):
        self.click_button('po')

    def at_button(self):
        self.click_button('at')

    def rn_button(self):
        self.click_button('rn')

    def fr_button(self):
        self.click_button('fr')

    def ra_button(self):
        self.click_button('ra')

    def lr_button(self):
        self.click_button('lr')

    def rf_button(self):
        self.click_button('rf')

    def db_button(self):
        self.click_button('db')

    def sg_button(self):
        self.click_button('sg')

    def bh_button(self):
        self.click_button('bh')

    def hs_button(self):
        self.click_button('hs')

    def mt_button(self):
        self.click_button('mt')

    def ds_button(self):
        self.click_button('ds')

    def rg_button(self):
        self.click_button('rg')

    def cn_button(self):
        self.click_button('cn')

    def nh_button(self):
        self.click_button('nh')

    def fl_button(self):
        self.click_button('fl')

    def mc_button(self):
        self.click_button('mc')

    def lv_button(self):
        self.click_button('lv')

    def ts_button(self):
        self.click_button('ts')

    def og_button(self):
        self.click_button('og')

    def ok(self):
        chemical_formula = str(self.ui.chemical_formula.text())
        molecular_mass, total_number_of_atoms = retrieving_molecular_mass_and_number_of_atoms_worked(chemical_formula)
        if molecular_mass and total_number_of_atoms:
            self.parent.material_ui = None

            if self.data_type == 'database':
                ui = self.database_window.list_ui[self.key]['value_label']
                ui.setText(chemical_formula)

            else:  # 'sample' or 'normalization'
                text_ui = self.parent.master_table_list_ui[self.key][self.data_type]['material']['text']
                text_ui.setText(chemical_formula)
                o_table = TableRowHandler(main_window=self.parent)
                o_table.transfer_widget_states(
                    from_key=self.key, data_type=self.data_type)
                self.parent.master_table_list_ui[self.key][self.data_type]['mass_density_infos']['molecular_mass'] \
                    = molecular_mass
                self.parent.master_table_list_ui[self.key][self.data_type]['mass_density_infos']['total_number_of_atoms'] \
                    = total_number_of_atoms

            self.parent.check_master_table_column_highlighting(
                column=self.column)
            self.close()
        else:
            self.ui.statusbar.setStyleSheet("color: red")
            self.ui.statusbar.showMessage("Unable to calculate Molecular Mass! CHECK YOUR FORMULA!",
                                          self.parent.statusbar_display_time)

    def check_status_save_button(self):
        if str(self.ui.chemical_formula.text()) != "":
            self.ui.save_button.setEnabled(True)
        else:
            self.ui.save_button.setEnabled(False)

    def cancel(self):
        self.parent.material_ui = None
        self.close()

    def closeEvent(self, c):
        self.parent.material_ui = None
        self.parent.material_ui_position = self.pos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    o_dialog = PeriodicTable()
    o_dialog.show()
    app.exec_()
