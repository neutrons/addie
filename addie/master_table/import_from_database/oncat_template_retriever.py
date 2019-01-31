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

    def isolate_relevant_information(self):
        template_information = {}
        for _index, _element in enumerate(self._oncat_default_template):
            _title = _element["name"]
            _path = _element["path"]
            template_information[_index] = {'title': _title,
                                            'path': _path}
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

        for _single_metadata in template:
            projection.append(_single_metadata['path'])

        return projection


