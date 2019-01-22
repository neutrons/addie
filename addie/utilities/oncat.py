import pyoncat

# Create token store
class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        pass

    def get_token(self):
        return self._token


def pyoncatGetRuns(oncat, instrument, runs, facility='SNS'):
    datafiles = oncat.Datafile.list(
        facility=facility,
        instrument=instrument,
        projection=['location'],
        tags=['type/raw'],
        exts=['.nxs.h5'],
        ranges_q='indexed.run_number:%d' % runs
    )
    return datafiles

def pyoncatGetIptsList(oncat=None, instrument='', facility='SNS'):
    ipts_list = oncat.Experiment.list(
        facility=facility,
        instrument=instrument,
        projection=['id']
    )
    return [ipts.name for ipts in ipts_list]


if __name__ == "__main__":
    useRcFile = True
    dashes = 35
    oncat = pyoncatForADDIE(useRcFile=useRcFile)

    print("-" * dashes)
    print("NOMAD file 11000")
    print("-" * dashes)
    datafiles = pyoncatGetRuns(oncat, 'NOM', 111000)
    for datafile in datafiles:
        print(datafile.location)

    print("-" * dashes)
    print("ARCS file 11000")
    print("-" * dashes)
    datafiles = pyoncatGetRuns(oncat, 'ARCS', 11000)
    for datafile in datafiles:
        print(datafile.location)

    print("-" * dashes)
    print("NOMAD IPTSs")
    print("-" * dashes)
    print(pyoncatGetIptsList(oncat, 'NOM'))

    print("-" * dashes)
    print("VISION IPTSs")
    print("-" * dashes)
    print(pyoncatGetIptsList(oncat, 'VIS'))