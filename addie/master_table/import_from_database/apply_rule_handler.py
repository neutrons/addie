class ApplyRuleHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def apply_global_rule(self):
        print(self.parent.global_rule_dict)

    def change_rule(self, is_added=False, is_removed=False, row=-1):
        """when user adds or removes a rule (criteria), we need to update the global rule dictionary"""
        if is_added:
            if self.parent.global_rule_dict == {}:
                # first time adding a rule = group
                _row_rule_dict = {}
                _row_rule_dict['name'] = "0"
                _row_rule_dict['list_rules'] = ['0']
                _row_rule_dict['inner_rule'] = 'and'
                _row_rule_dict['outer_rule'] = None
                self.parent.global_rule_dict = {'0': _row_rule_dict}
            else:
                # not the first time adding a rule
                # add a group of just this new rule
                pass
        else:
            # remove the rule from all the groups
            pass

