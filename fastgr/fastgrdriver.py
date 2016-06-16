import os
import sys
import numpy as np

# add a python path for local development
sys.path.append('/Users/wzz/MantidBuild/debug/bin/')

import mantid.simpleapi as simpleapi
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
        # dictionary to record workspace index of a certain S(Q)
        self._sqIndexDict = dict()

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
        string as G(r) workspace's name
        """
        # check
        assert min_r < max_r, 'Rmin must be less than Rmax (%f >= %f)' % (min_r, max_r)
        assert delta_r < (max_r - min_r), 'Must have more than one bin in G(r) (%f >= %f)' \
                                          '' % (delta_r, (max_r - min_r))

        assert min_q < max_q, 'Qmin must be less than Qmax (%f >= %f)' % (min_q, max_q)

        # set up the parameters for FourierTransform
        # output workspace
        gr_ws_name = 'G(R)_%s_%d' % (self._currSqWsName, self._sqIndexDict[self._currSqWsName])
        kwargs = {'OutputWorkspace': gr_ws_name,
                  'Qmin': min_q,
                  'Qmax': max_q,
                  'PDFType': 'G(r)',
                  'DeltaR': delta_r,
                  'Rmax': max_r}

        # get the input unit
        sq_ws = AnalysisDataService.retrieve(self._currSqWsName)
        sofq_type = 'S(Q)'

        # do the FFT
        print '[DB]: Input Sof Q Type = |', sq_ws.YUnitLabel(), '|'
        simpleapi.PDFFourierTransform(InputWorkspace=self._currSqWsName,
                                      InputSofQType=sofq_type,
                                      **kwargs)

        # check
        assert AnalysisDataService.doesExist(gr_ws_name), 'Failed to do Fourier Transform.'
        self._grWsNameDict[(min_q, max_q)] = gr_ws_name

        # update state variable
        self._sqIndexDict[self._currSqWsName] += 1

        return gr_ws_name

    def conjoin_banks(self):
        """
        Conjoin all 6 single banks
        Returns:

        """
        simpleapi.ConjoinWorkspaces()

        return

    @staticmethod
    def get_bragg_data(bank, x_unit):
        """ Get Bragg diffraction data of 1 bank
        Args:
            bank:

        Returns:
        3-tuple of numpy 1D array for X, Y and E
        """
        # check
        assert isinstance(bank, int) and bank > 0

        # construct bank workspace name
        ws_name = 'bank%d' % bank
        assert AnalysisDataService.doesExist(ws_name), 'Workspace %s does not exist.' % ws_name

        if x_unit != 'TOF':
            bank_ws = AnalysisDataService.retrieve(ws_name)
            curr_unit = bank_ws.getAxis(0).getUnitID()
            if curr_unit != x_unit:
                simpleapi.ConvertUnit(InputWorkspace=ws_name, OutputWorkspace=ws_name,
                                      TargetUnit=x_unit)

        # convert to point data for plotting
        simpleapi.ConvertToPointData(InputWorkspace=ws_name, OutputWorkspace=ws_name)

        # get workspace
        bank_ws = AnalysisDataService.retrieve(ws_name)

        return bank_ws.readX(0), bank_ws.readY(0), bank_ws.readE(0)

    def get_current_workspaces(self):
        """
        Get current workspaces' names
        Returns
        -------
        a list of strings
        """
        return AnalysisDataService.getObjectNames()

    def get_gr(self, min_q, max_q):
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
        assert ((min_q, max_q)) in self._grWsNameDict, error_msg

        # get the workspace
        gr_ws_name = self._grWsNameDict[(min_q, max_q)]
        gr_ws = AnalysisDataService.retrieve(gr_ws_name)

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

    @staticmethod
    def load_bragg_file(file_name):
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
            simpleapi.LoadGSS(Filename=file_name,
                        OutputWorkspace=gss_ws_name)
        elif base_file_name.endswith('.dat'):
            simpleapi.LoadAscii(Filename=file_name,
                          OutputWorkspace=gss_ws_name,
                          Unit='TOF')
        else:
            raise RuntimeError('File %s is not of a supported type.' % file_name)

        # check
        assert AnalysisDataService.doesExist(gss_ws_name)

        return gss_ws_name

    def load_sq(self, file_name):
        """
        Load S(Q) to a numpy
        Guarantees: the file is loaded to self._currSQX, _currSQY and _currSQE
        Parameters
        ----------
        file_name :: name of the S(Q)

        Returns
        -------
        2-tuple range of Q
        """
        out_ws_name = os.path.basename(file_name).split('.')[0]

        simpleapi.LoadAscii(Filename=file_name, OutputWorkspace=out_ws_name, Unit='MomentumTransfer')
        assert AnalysisDataService.doesExist(out_ws_name), 'Unable to load S(Q) file %s.' % file_name

        # set to the current S(Q) workspace name
        self._currSqWsName = out_ws_name
        self._sqIndexDict[self._currSqWsName] = 0

        # get range of Q from the loading
        sq_ws = AnalysisDataService.retrieve(out_ws_name)
        q_min = sq_ws.readX(0)[0]
        q_max = sq_ws.readX(0)[-1]

        return q_min, q_max

    def split_to_single_bank(self, gss_ws_name):
        """
        Split a multiple-bank GSAS workspace to a set of single-spectrum MatrixWorkspace
        Parameters
        ----------
        gss_ws_name

        Returns
        -------
        Name of grouped workspace
        """
        # check
        assert isinstance(gss_ws_name, str)
        assert AnalysisDataService.doesExist(gss_ws_name)

        # get workspace
        gss_ws = AnalysisDataService.retrieve(gss_ws_name)

        ws_list = list()

        if gss_ws.getNumberHistograms() == 1:
            # input is already a single-spectrum workspace
            ws_list.append(gss_ws_name)
        else:
            num_spec = gss_ws.getNumberHistograms()

            for i_ws in range(num_spec):
                # split this one to a single workspace
                out_ws_name = 'bank%d' % (i_ws+1)
                # also can use ExtractSpectra()
                simpleapi.CropWorkspace(InputWorkspace=gss_ws_name,
                                  OutputWorkspace=out_ws_name,
                                  StartWorkspaceIndex=i_ws, EndWorkspaceIndex=i_ws)
                assert AnalysisDataService.doesExist(out_ws_name)
                ws_list.append(out_ws_name)
            # END-FOR
        # END-IF

        # group all the workspace
        ws_group_name = gss_ws_name + '_group'
        simpleapi.GroupWorkspaces(InputWorkspaces=ws_list,
                            OutputWorkspace=ws_group_name)

        return ws_group_name
