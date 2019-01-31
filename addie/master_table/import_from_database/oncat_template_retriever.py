from collections import OrderedDict

from addie.utilities.oncat import pyoncatGetTemplate


class OncatTemplateRetriever:
    """Retrieves the up to date ONCat template of the given instrument. The needed information
    are then retrieved from the template such as column name and path to oncat database. The
    output of this class is a dictionary with those informations."""

    template_information = OrderedDict()   # {'Run #': 'indexed.run_number',
                                           #  'ITEMS ID': 'metadata.entry.sample.identifier',
                                           #  ...,
                                           # }
    _oncat_default_template = {}

    def __init__(self, parent=None):
        self.parent = parent

        self.retrieve_template()
        self.isolate_relevant_information()

    def retrieve_template(self):
        instrument = self.parent.instrument['short_name']
        facility = self.parent.facility

        _template = pyoncatGetTemplate(oncat=self.parent.oncat,
                                       instrument=instrument,
                                       facility=facility)

        _default_template = _template[0]["columns"]
        self._oncat_default_template = _default_template

    def isolate_relevant_information(self):
        template_information = OrderedDict()
        for _element in self._oncat_default_template:
            _title = _element["name"]
            _path = _element["path"]
            template_information[_title] = _path
        self.template_information = template_information

    def get_template_information(self):
        return self.template_information