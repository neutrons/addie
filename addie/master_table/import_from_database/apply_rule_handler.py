class ApplyRuleHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def apply_global_rule(self):
        print(self.parent.global_rule_dict)