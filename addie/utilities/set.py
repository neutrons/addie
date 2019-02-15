class Set:

    def __init__(self, parent=None):
        self.parent = parent

    def set_instrument(self, short_name='', full_name=''):

        if short_name:
            try:
                index = self.parent.list_instrument["short_name"].index(short_name)
            except ValueError:
                return

            self.parent.instrument["short_name"] = short_name
            self.parent.instrument["full_name"] = self.parent.list_instrument["full_name"][index]

        else:
            try:
                index = self.parent.list_instrument["full_name"].index(full_name)
            except ValueError:
                return

            self.parent.instrument["full_name"] = full_name
            self.parent.instrument["short_name"] = self.parent.list_instrument["short_name"][index]
