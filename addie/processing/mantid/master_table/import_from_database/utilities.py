from __future__ import (absolute_import, division, print_function)

from addie.utilities.list_runs_parser import ListRunsParser


def get_list_of_runs_found_and_not_found(str_runs="",
                                         oncat_result={},
                                         check_not_found=True):
    """This method compare the list of runs from the string passed in, to the
    output produced by oncat. If a run is in the two inputs, it means it has
    been found, if not, it hasn't been found"""

    if str_runs:
        o_parser = ListRunsParser(current_runs=str_runs)
        list_of_runs = o_parser.list_current_runs
    else:
        check_not_found = False

    list_of_runs_found = []
    for _json in oncat_result:
        _run_number = _json['indexed']['run_number']
        list_of_runs_found.append("{}".format(_run_number))

    if check_not_found:
        list_of_runs_not_found = set(list_of_runs) - set(list_of_runs_found)
    else:
        list_of_runs_not_found = []

    return {'not_found': list_of_runs_not_found,
            'found': list_of_runs_found}
