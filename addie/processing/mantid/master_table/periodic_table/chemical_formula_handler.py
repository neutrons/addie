from __future__ import (absolute_import, division, print_function)


def format_chemical_formula_equation(raw_chemical_formula='N/A'):
    """chemical formula defined at the DAS level, and saved in ONCat and then the json do not always have the
    format that allow us to calculate the mass density. This method will try to force the format of this equation"""

    if raw_chemical_formula == 'N/A':
        return raw_chemical_formula

    if raw_chemical_formula.lower() == 'none':
        return 'N/A'

    list_of_formula = list(raw_chemical_formula)
    clean_list = []
    for _c in list_of_formula:
        if _c.istitle():
            clean_list.append(" ")
        clean_list.append(_c)

    clean_formula = "".join(clean_list).strip()
    return clean_formula
