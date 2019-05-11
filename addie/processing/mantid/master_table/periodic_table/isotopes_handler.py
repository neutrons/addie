from __future__ import (absolute_import, division, print_function)
import periodictable
from qtpy.QtWidgets import QDialog
from addie.utilities import load_ui

#from addie.ui_isotopes import Ui_Dialog as UiDialog


class IsotopesHandler:

    def __init__(self, parent=None, element=''):

        if parent.isotope_ui is None:
            o_isotope = IsotopeDialog(parent=parent,
                                      element=element)
            o_isotope.show()
            parent.isotope_ui = o_isotope
        else:
            parent.isotope_ui.setFocus()
            parent.isotope_ui.activateWindow()


class IsotopeDialog(QDialog):

    def __init__(self, parent=None, element=''):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('isotopes.ui', baseinstance=self)

        self.init_widgets(element)

    def init_widgets(self, element):
        list_isotopes = [element]
        for iso in getattr(periodictable, element):
            #reformat
            list_str_iso = str(iso).split('-')
            str_iso = "".join(list_str_iso[::-1])
            list_isotopes.append(str_iso)

        self.ui.comboBox.addItems(list_isotopes)

    def accept(self):
        isotope_selected = self.ui.comboBox.currentText()
        isotope_number = self.ui.number_of_elements.value()
        is_natural_element = False
        if self.ui.comboBox.currentIndex() == 0:
            is_natural_element = True
        self.parent.add_new_entry(isotope=isotope_selected,
                                  number=isotope_number,
                                  is_natural_element=is_natural_element)
        self.close()
        self.parent.isotope_ui = None

    def reject(self):
        self.close()
        self.parent.isotope_ui = None

    def closeEvent(self, c):
        pass
