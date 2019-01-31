import numpy as np

from addie.utilities.oncat import pyoncatGetTemplate


class OncatTemplateRetriever:
    """Retrieves the up to date ONCat template of the given instrument. The needed information
    are then retrieved from the template such as column name and path to oncat database. The
    output of this class is a dictionary with those informations."""

    template_information = {}   # {'0': {'title': 'Run #', 'path': 'indexed.run_number'},
                                #  '1':  ....
                                # }
    _oncat_default_template = {}

    def __init__(self, parent=None):
        self.parent = parent

        self.retrieve_template()
        self.isolate_relevant_information()

    def retrieve_template(self):
        instrument = self.parent.instrument['short_name']
        facility = self.parent.facility

        list_templates = pyoncatGetTemplate(oncat=self.parent.oncat,
                                       instrument=instrument,
                                       facility=facility)

        for template in list_templates:
            if hasattr(template, "default"):
                if template.default:
                    self._oncat_default_template = template["columns"]
                    return

        _default_template = list_templates[0]["columns"]
        self._oncat_default_template = _default_template

        import pprint
        pprint.pprint(_default_template)

    def isolate_relevant_information(self):
        """from all the information provided by the ONCat template, we are only interested by the following infos
        [name, path and units]. We isolate those into the template_information dictionary"""
        template_information = {}
        for _index, _element in enumerate(self._oncat_default_template):
            _title = _element["name"]
            _path = _element["path"]
            if "units" in _element:
                _units = _element["units"]
            else:
                _units = ""
            template_information[_index] = {'title': _title,
                                            'path': _path,
                                            'units': _units}
        self.template_information = template_information

    def get_template_information(self):
        return self.template_information

    @staticmethod
    def create_oncat_projection_from_template(with_location=False,
                                              template={}):
        """Using the ONCat template to create projection used by oncat
        to return full information"""

        projection = []
        if with_location:
            projection = ['location']

        nbr_columns = len(template)
        for _col in np.arange(nbr_columns):
            projection.append(template[_col]['path'])

        return projection


