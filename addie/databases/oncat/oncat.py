from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QDialog
from addie.utilities import load_ui


# Create token store
class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        pass

    def get_token(self):
        return self._token


def pyoncatGetNexus(oncat=None,
                    instrument='',
                    runs=-1,
                    facility='SNS',
                    projection=[]):

    if projection == []:
        projection = ['location',
                      'indexed.run_number',
                      'metadata.entry.sample.chemical_formula',
                      'metadata.entry.sample.mass_density',
                      'metadata.entry.title',
                      'metadata.entry.proton_charge',
                      'metadata.entry.daslogs.bl1b:se:sampletemp.device_name'
                      ]

    datafiles = oncat.Datafile.list(
        facility=facility,
        instrument=instrument,
        projection=projection,
        tags=['type/raw'],
        exts=['.nxs.h5', '.nxs'],
        ranges_q='indexed.run_number:%s' % runs
    )
    return datafiles


def pyoncatGetTemplate(oncat=None,
                       instrument='',
                       facility='SNS'):
    all_templates = oncat.Template.list(facility=facility,
                                        instrument=instrument,
                                        )
    return all_templates


def pyoncatGetRunsFromIpts(oncat=None,
                           instrument='',
                           ipts='',
                           facility='SNS',
                           projection=[]):

    if projection == []:
        projection = ['indexed.run_number',
                      'metadata.entry.sample.chemical_formula',
                      'metadata.entry.sample.mass_density',
                      'metadata.entry.title',
                      'metadata.entry.proton_charge',
                      'metadata.entry.daslogs.bl1b:se:sampletemp.device_name'
                      ]

    run_list = oncat.Datafile.list(facility=facility,
                                   instrument=instrument,
                                   experiment=ipts,
                                   projection=projection,
                                   tags=['type/raw'],
                                   exts=['.nxs.h5', '.nxs'])
    return run_list


def pyoncatGetIptsList(oncat=None,
                       instrument='',
                       facility='SNS'):
    ipts_list = oncat.Experiment.list(
        facility=facility,
        instrument=instrument,
        projection=['id']
    )
    return [ipts.id for ipts in ipts_list]

# if __name__ == "__main__":
#     useRcFile = True
#     dashes = 35
#     oncat = pyoncatForADDIE(useRcFile=useRcFile)
#
#     print("-" * dashes)
#     print("NOMAD file 11000")
#     print("-" * dashes)
#     datafiles = pyoncatGetRuns(oncat, 'NOM', 111000)
#     for datafile in datafiles:
#         print(datafile.location)
#
#     print("-" * dashes)
#     print("ARCS file 11000")
#     print("-" * dashes)
#     datafiles = pyoncatGetRuns(oncat, 'ARCS', 11000)
#     for datafile in datafiles:
#         print(datafile.location)
#
#     print("-" * dashes)
#     print("NOMAD IPTSs")
#     print("-" * dashes)
#     print(pyoncatGetIptsList(oncat, 'NOM'))
#
#     print("-" * dashes)
#     print("VISION IPTSs")
#     print("-" * dashes)
#     print(pyoncatGetIptsList(oncat, 'VIS'))


class OncatErrorMessageWindow(QDialog):

    def __init__(self, parent=None, list_of_runs=[], message=''):
        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('oncat_error_message.ui', baseinstance=self)
        self.init_widgets(list_of_runs=list_of_runs)
        self.ui.message.setText(message)

    def init_widgets(self, list_of_runs=[]):
        str_list_of_runs = "\n".join(list_of_runs)
        self.ui.list_of_runs.setText(str_list_of_runs)
