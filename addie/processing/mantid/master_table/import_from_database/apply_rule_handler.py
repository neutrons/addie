from __future__ import (absolute_import, division, print_function)

import collections
import numpy as np

from addie.processing.mantid.master_table.import_from_database.gui_handler import FilterTableHandler, FilterResultTableHandler


class ApplyRuleHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def apply_global_rule(self):
        self.retrieve_list_of_rows_for_each_rule()
        self.apply_inner_rules()
        self.apply_outer_rules()
        self.update_tableWidget_filter_result()

    def update_tableWidget_filter_result(self):
        list_of_rows_to_show = self.parent.list_of_rows_with_global_rule
        nbr_row = self.parent.ui.tableWidget_filter_result.rowCount()
        for _row in np.arange(nbr_row):
            hide_row = True
            if _row in list_of_rows_to_show:
                hide_row = False
            self.parent.ui.tableWidget_filter_result.setRowHidden(_row, hide_row)

    def retrieve_list_of_rows_for_each_rule(self):
        global_rule_dict = self.parent.global_rule_dict

        for _group_key in global_rule_dict.keys():
            _group = global_rule_dict[_group_key]
            list_of_rules_for_this_group = _group['list_rules']

            list_of_rows_for_each_rule = {}  # {'0': [0,1,2,3,4], '1':[2,3,4,5] ...}

            for _rule in list_of_rules_for_this_group:
                list_of_rows_matching_rule = self.get_list_of_rows_matching_rule(rule_index=_rule)
                list_of_rows_for_each_rule[_rule] = list_of_rows_matching_rule

            global_rule_dict[_group_key]['list_of_rows'] = list_of_rows_for_each_rule

        self.parent.global_rule_dict = global_rule_dict

    def apply_inner_rules(self):
        """within each group, check the inner rule (and, or) and save the corresponding list of rows that
        follow that rule"""
        global_rule_dict = self.parent.global_rule_dict

        for _group_key in global_rule_dict.keys():
            _group = global_rule_dict[_group_key]

            inner_rule = _group['inner_rule']

            is_first_list_of_rows = True
            for _rule_key in _group['list_of_rows'].keys():
                if is_first_list_of_rows:
                    list_of_rows_with_inner_rule = set(_group['list_of_rows'][_rule_key])
                    is_first_list_of_rows = False
                else:
                    new_list_of_rows = set(_group['list_of_rows'][_rule_key])

                    if inner_rule == 'and':
                        list_of_rows_with_inner_rule = list_of_rows_with_inner_rule & new_list_of_rows
                    else:
                        list_of_rows_with_inner_rule = list_of_rows_with_inner_rule | new_list_of_rows

            global_rule_dict[_group_key]['inner_list_of_rows'] = list_of_rows_with_inner_rule

        self.parent.global_rule_dict = global_rule_dict

    def apply_outer_rules(self):
        global_rule_dict = self.parent.global_rule_dict

        is_first_group = True
        list_of_rows_with_outer_rule = set()
        for _group_key in global_rule_dict.keys():
            _group = global_rule_dict[_group_key]

            if is_first_group:
                list_of_rows_with_outer_rule = _group['inner_list_of_rows']
                is_first_group = False
            else:
                new_list_of_rows = _group['inner_list_of_rows']

                outer_rule = _group['outer_rule']
                if outer_rule == 'and':
                    list_of_rows_with_outer_rule = list_of_rows_with_outer_rule & new_list_of_rows
                else:
                    list_of_rows_with_outer_rule = list_of_rows_with_outer_rule | new_list_of_rows

        self.parent.list_of_rows_with_global_rule = list_of_rows_with_outer_rule

    def get_list_of_rows_matching_rule(self, rule_index=-1):
        """This method will retrieve the rule definition, for example
                item: sample formula
                logic: is
                text: Si
            meaning that the Sample formula must be Si to accept this row
        """
        table_handler = FilterTableHandler(table_ui=self.parent.ui.tableWidget)
        row = table_handler.return_first_row_for_this_item_value(string_to_find=str(rule_index),
                                                                 column_to_look_for=1)

        keyword_name = table_handler.get_keyword_name(row=row)
        criteria = table_handler.get_criteria(row=row)
        string_to_find = table_handler.get_string_to_look_for(row=row)

        result_table_handler = FilterResultTableHandler(table_ui=self.parent.ui.tableWidget_filter_result)
        column_where_to_look_for = result_table_handler.get_column_of_given_keyword(keyword=keyword_name)

        list_of_rows = result_table_handler.get_rows_of_matching_string(column_to_look_for=column_where_to_look_for,
                                                                        string_to_find=string_to_find,
                                                                        criteria=criteria)

        return list_of_rows

    def change_rule(self, is_added=False, is_removed=False, row=-1):
        """when user adds or removes a rule (criteria), we need to update the global rule dictionary"""
        if is_added:
            _row_rule_dict = {}
            if self.parent.global_rule_dict == {}:
                # first time adding a rule = group
                _row_rule_dict['group_name'] = "0"
                _row_rule_dict['list_rules'] = ['0']
                _row_rule_dict['inner_rule'] = 'and'
                _row_rule_dict['outer_rule'] = None
                self.parent.global_rule_dict = collections.OrderedDict()
                self.parent.global_rule_dict['0'] =_row_rule_dict
            else:
                # not the first time adding a rule
                # add a group of just this new rule
                name_of_new_rule = str(self.parent.ui.tableWidget.item(row, 1).text())
                name_of_group = self.get_name_of_group()
                _row_rule_dict['group_name'] = name_of_group
                _row_rule_dict['list_rules'] = [name_of_new_rule]
                _row_rule_dict['inner_rule'] = 'and'
                _row_rule_dict['outer_rule'] = 'and'
                self.parent.global_rule_dict[name_of_group] = _row_rule_dict

        else:
            # remove the rule from all the groups
            name_of_rule_to_remove = str(self.parent.ui.tableWidget.item(row, 1).text())
            self.remove_rule_from_global_rule_dict(name_of_rule_to_remove = name_of_rule_to_remove)

    def remove_rule_from_global_rule_dict(self, name_of_rule_to_remove=None):
        global_rule_dict = self.parent.global_rule_dict
        for _key in list(global_rule_dict.keys()):
            _list_of_rule = global_rule_dict[_key]['list_rules']
            new_list_of_rules = [_rule for _rule in _list_of_rule if _rule != name_of_rule_to_remove]
            if new_list_of_rules == []:
                _ = global_rule_dict.pop(_key, None)
            else:
                global_rule_dict[_key]['list_rules'] = new_list_of_rules

        self.parent.global_rule_dict = global_rule_dict

    def get_name_of_group(self):
        # using the current list of groups, this method returns the first index (str) available to name the new group.
        global_rule_dict = self.parent.global_rule_dict
        available_global_rule_index = '0'
        list_of_keys = list(global_rule_dict.keys())
        while True:
            if available_global_rule_index in list_of_keys:
                available_global_rule_index = str(np.int(available_global_rule_index) + 1)
            else:
                return available_global_rule_index

    def create_global_rule_string(self):
        global_rule_string = ''
        global_rule_dict = self.parent.global_rule_dict

        is_first_group = True
        # looping through the groups

        for _group_index in global_rule_dict.keys():

            # list of rules for this group
            _list_rules = global_rule_dict[_group_index]['list_rules']

            # adding '#' in front of each rule name for this group
            _str_list_rules = ["#{}".format(_rule) for _rule in _list_rules]

            # keeping record of the number of rules to see if we need or not to specify inner logic
            nbr_rules = len(_list_rules)
            _inner_rule = " " + global_rule_dict[_group_index]['inner_rule'] +  " "
            str_rule_for_this_group = _inner_rule.join(_str_list_rules)

            if nbr_rules > 1:
                str_rule_for_this_group = "( " + str_rule_for_this_group + " )"

            if is_first_group and (str_rule_for_this_group != ""):
                global_rule_string = str_rule_for_this_group
                is_first_group = False
            elif str_rule_for_this_group != "":
                _outer_logic = global_rule_dict[_group_index]['outer_rule']
                global_rule_string = "{} {} {}".format(global_rule_string, _outer_logic, str_rule_for_this_group)

        return global_rule_string
