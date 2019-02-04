import collections
import numpy as np


class ApplyRuleHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def apply_global_rule(self):
        print(self.parent.global_rule_dict)

    def change_rule(self, is_added=False, is_removed=False, row=-1):
        """when user adds or removes a rule (criteria), we need to update the global rule dictionary"""
        if is_added:
            _row_rule_dict = {}
            if self.parent.global_rule_dict == {}:
                # first time adding a rule = group
                _row_rule_dict['name'] = "0"
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
                _row_rule_dict['name'] = name_of_group
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
        for _key in global_rule_dict.keys():
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

