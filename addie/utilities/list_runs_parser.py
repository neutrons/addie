import numpy as np
import itertools


class ListRunsParser(object):
    """
    will clean up the current_list_of_runs with the new added runs
    ex: [1,2,3,4,7] -> 1-4,7
    if a new run is already in the list of runs, it will then be removed from the list
    ex: [1,2,3,4] with new run [1] -> 2-4
    """

    list_current_runs = []  # ['1','10','2','30','4']
    int_list_current_runs = []  # [1, 2, 4, 10, 30]

    def __init__(self, current_runs=''):
        if current_runs:
            self.make_discrete_list_of_runs(str_current_runs=current_runs)

    def make_discrete_list_of_runs(self, str_current_runs=''):
        """this method allows a combine list of runs (1-4,7) into the expanded version (1,2,3,4,7)"""
        spans = (el.partition('-')[::2] for el in str_current_runs.split(','))
        ranges = (np.arange(int(s), int(e) + 1 if e else int(s) + 1)
                  for s, e in spans)
        try:
            all_nums = itertools.chain.from_iterable(ranges)
            _all_nums = set(all_nums)
        except ValueError:
            raise ValueError("Check format of input")
        self.list_current_runs = [str(_run) for _run in _all_nums]

    def new_runs(self, list_runs=[]):
        """add new runs, remove already existing ones
        This also creates the compact version of the list
        ex: "1,2,3,4,5,6,10,15" -> "1-6,10,15"
        """

        # find list of runs to remove
        list_runs = set(list_runs)
        _list_runs_to_remove = set(list_runs.intersection(self.list_current_runs))

        # remove the runs from list_runs and list_current_runs
        clean_list_runs = list(list_runs - _list_runs_to_remove)
        clean_list_current_runs = list(set(self.list_current_runs) - _list_runs_to_remove)

        new_list_current_runs = clean_list_runs + clean_list_current_runs
        self.list_current_runs = new_list_current_runs

        # go from string to int
        int_new_list_current_runs = [np.int(_run) for _run in new_list_current_runs]

        # sort them to prepare them for output format
        int_new_list_current_runs.sort()
        self.int_list_current_runs = int_new_list_current_runs

        if int_new_list_current_runs == []:
            self.str_list_current_runs = ""
            return

        # create output string format

        # only 1 run
        if len(int_new_list_current_runs) == 1:
            self.str_list_current_runs = str(int_new_list_current_runs[0])
            return str(int_new_list_current_runs[0])

        # more than 1 run

        # create full matching list
        def match_list(reference_list=[], our_list=[]):
            _index = 0
            _ref_list_and_our_list = zip(our_list, reference_list)
            for _ref_run, _our_run in _ref_list_and_our_list:
                if _ref_run == _our_run:
                    _index += 1
                    continue
                break

            return _index

        _index = 0
        _groups = []
        _our_list = self.int_list_current_runs[_index: ]
        _list_full_reference = np.arange(_our_list[0], _our_list[-1]+1)

        # print("new list: {}".format(_our_list))

        while _our_list:

            _ref_index = match_list(reference_list=_list_full_reference,
                                    our_list=_our_list)

            _group = [_our_list[0], _our_list[_ref_index-1]]
            # print("_group: {}".format(_group))
            _groups.append(_group)

            _our_list = _our_list[_ref_index:]
            if len(_our_list) == 1:
                _groups.append(_our_list)
                break

            if len(_our_list) == 0:
                break

            _list_full_reference = np.arange(_our_list[0], _our_list[-1]+1)

        # print("_groups: {}".format(_groups))

        list_runs = []
        for _group in _groups:

            if len(_group) == 2:
                [_left_value, _right_value] = _group

                if _left_value == _right_value:
                    list_runs.append(str(_left_value))
                elif _right_value == (_left_value + 1):
                    list_runs.append(str(_left_value))
                    list_runs.append(str(_right_value))
                else:
                    list_runs.append("{}-{}".format(_left_value, _right_value))

            else:
                list_runs.append(str(_group[0]))

        str_runs = ",".join(list_runs)
        # print(str_runs)
        return str_runs
