import os
import numpy as np
import mantid.simpleapi as mtd
from mantid.api import AnalysisDataService


class FastGRDriver(object):
    """
    Driver for FastGR application
    """
    def __init__(self):
        """ Initialization
        Returns
        -------

        """
        # name of the MatrixWorkspace for S(Q)
        self._currSqWsName = ''

        # dictionary of the workspace with rmin, rmax and delta r setup
        self._grWsIndex = 0
        self._grWsNameDict = dict()

        return

    def calculate_gr(self, min_r, delta_r, max_r, min_q, max_q):
        """
        Calculate G(R)
        Parameters
        ----------
        min_r :: R_min
        delta_r :: delta R
        max_r
        min_q
        max_q

        Returns
        -------
        None
        """
        # check
        assert min_r < max_r, 'Rmin must be less than Rmax (%f >= %f)' % (min_r, max_r)
        assert delta_r < (max_r - min_r), 'Must have more than one bin in G(r) (%f >= %f)' \
                                          '' % (delta_r, (max_r - min_r))

        assert min_q < max_q, 'Qmin must be less than Qmax (%f >= %f)' % (min_q, max_q)

        # set up the parameters for FourierTransform
        # output workspace
        gr_ws_name = 'G(R)_%s' % self._currSqWsName
        kwargs = {'OutputWorkspace': gr_ws_name,
                  'Qmin': min_q,
                  'Qmax': max_q,
                  'PDFType': 'G(r)',
                  'DeltaR': delta_r,
                  'Rmax': max_r}

        # get the input unit
        sq_ws = AnalysisDataService.retrieve(self._currSqWsName)
        inputsofqtype = sq_ws.YUnitLabel()
        # FIXME/TODO - Need a GUI widget to select from G(r), g(r), RDF(r)
        inputsofqtype = 'S(Q)'

        # do the FFT
        print '[DB]: Input Sof Q Type = |', sq_ws.YUnitLabel(), '|'
        mtd.PDFFourierTransform(InputWorkspace=self._currSqWsName,
                                InputSofQType=inputsofqtype,
                                **kwargs)

        # check
        assert AnalysisDataService.doesExist(gr_ws_name), 'Failed to do Fourier Transform.'
        self._grWsNameDict[(min_r, max_r, delta_r)] = gr_ws_name

        return

    def get_gr(self, min_r, delta_r, max_r):
        """ Get G(r)
        Parameters
        ----------
        min_r
        delta_r
        max_r

        Returns
        -------
        3-tuple for numpy.array
        """
        # check... find key in dictionary
        error_msg = 'R-range and delta R are not support. Current stored G(R) parameters are %s.' \
                    '' % str(self._grWsNameDict.keys())
        assert (min_r, max_r, delta_r) in self._grWsNameDict, error_msg

        # get the workspace
        gr_ws = AnalysisDataService.retrieve((min_r, max_r, delta_r))

        return gr_ws.readX(0), gr_ws.readY(0), gr_ws.readE(0)

    def get_sq(self):
        """
        Get S(Q)
        Returns
        -------
        3-tuple of numpy array as Q, S(Q) and Sigma(Q)
        """
        assert AnalysisDataService.doesExist(self._currSqWsName), 'S(Q) matrix workspace %s does not exist.' \
                                                                  '' % self._currSqWsName

        out_ws = AnalysisDataService.retrieve(self._currSqWsName)

        return out_ws.readX(0), out_ws.readY(0), out_ws.readE(0)

    def load_bragg_file(self, file_name):
        """
        Load Bragg diffraction file (including 3-column data file, GSAS file) for Rietveld
        Parameters
        ----------
        file_name

        Returns
        -------

        """
        # load with different file type
        base_file_name = os.path.basename(file_name).lower()
        gss_ws_name = os.path.basename(file_name).split('.')[0]
        if base_file_name.endswith('.gss') or base_file_name.endswith('.gsa'):
            mtd.LoadGSS(Filename=file_name,
                        OutputWorkspace=gss_ws_name)
        elif base_file_name.endswith('.dat'):
            mtd.LoadAscii(Filename=file_name,
                          OutputWorkspace=gss_ws_name,
                          Unit='TOF')
        else:
            raise RuntimeError('File %s is not of a supported type.' % file_name)

        # check
        assert AnalysisDataService.doesExist(gss_ws_name)

        return

    def load_sq(self, file_name):
        """
        Load S(Q) to a numpy
        Guarantees: the file is loaded to self._currSQX, _currSQY and _currSQE
        Parameters
        ----------
        file_name :: name of the S(Q)

        Returns
        -------
        2-tuple as load-status, error-mesage
        """
        out_ws_name = os.path.basename(file_name).split('.')[0]

        mtd.LoadAscii(Filename=file_name,
                      OutputWorkspace=out_ws_name,
                      Unit='MomentumTransfer')
        assert AnalysisDataService.doesExist(out_ws_name), 'Unable to load S(Q) file %s.' % file_name

        self._currSqWsName = out_ws_name

        return

