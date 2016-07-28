import os
import sys
import math
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

        # dictionary to manage the GSAS data
        # key: ws_group_name, value: (gss_ws_name, ws_list).  it is in similar architecture with tree
        self._braggDataDict = dict()

        return

    def calculate_gr(self, sq_ws_name, pdf_type, min_r, delta_r, max_r, min_q, max_q):
        """
        Calculate G(R)
        Parameters
        ----------
        sq_ws_name :: workspace name of S(q)
        pdf_type :: type of PDF as G(r), g(r) and RDF(r)
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
        assert isinstance(sq_ws_name, str) and AnalysisDataService.doesExist(sq_ws_name)
        assert isinstance(pdf_type, str) and len(pdf_type) > 0, \
            'PDF type is %s is not supported.' % str(pdf_type)
        assert min_r < max_r, 'Rmin must be less than Rmax (%f >= %f)' % (min_r, max_r)
        assert delta_r < (max_r - min_r), 'Must have more than one bin in G(r) (%f >= %f)' \
                                          '' % (delta_r, (max_r - min_r))

        assert min_q < max_q, 'Qmin must be less than Qmax (%f >= %f)' % (min_q, max_q)

        # set to the current S(q) workspace name
        self._currSqWsName = sq_ws_name

        # set up the parameters for FourierTransform
        # output workspace
        prefix = 'G'
        if pdf_type.startswith('g'):
            prefix = 'g'
        elif pdf_type.startswith('r'):
            prefix = 'RDF'

        gr_ws_name = '%s(R)_%s_%d' % (prefix, self._currSqWsName, self._sqIndexDict[self._currSqWsName])
        kwargs = {'OutputWorkspace': gr_ws_name,
                  'Qmin': min_q,
                  'Qmax': max_q,
                  'PDFType': pdf_type,
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

    def delete_workspace(self, workspace_name):
        """
        Delete a workspace from Mantid's AnalysisDataService
        Args:
            workspace_name: name of a workspace as a string instance

        Returns: None

        """
        # check
        assert isinstance(workspace_name, str), \
            'Input workspace name must be a string, but not %s.' % str(type(workspace_name))
        assert AnalysisDataService.doesExist(workspace_name), 'Workspace %s does not exist.' % workspace_name

        # delete
        simpleapi.DeleteWorkspace(Workspace=workspace_name)

        return

    @staticmethod
    def conjoin_banks(ws_name_list, output_ws_name):
        """
        Conjoin all 6 single banks
        Args:
            ws_name_list: list of workspaces' names for conjoining
            output_ws_name: name of the output workspace
        Returns:

        """
        # check inputs
        assert isinstance(ws_name_list, list) and len(ws_name_list) > 1, \
            'There must be at least 2 workspaces for conjoining operation.'
        assert isinstance(output_ws_name, str)

        # clone the first workspace for the output workspace
        assert AnalysisDataService.doesExist(ws_name_list[0])
        simpleapi.CloneWorkspace(InputWorkspace=ws_name_list[0],
                                 OutputWorkspace=output_ws_name)

        for i_ws in range(1, len(ws_name_list)):
            simpleapi.ConjoinWorkspaces(InputWorkspace1=output_ws_name,
                                        InputWorkspace2=ws_name_list[i_ws])
        # END-FOR(i_ws)

        return

    def get_bragg_data(self, ws_group_name, bank_id, x_unit):
        """ Get Bragg diffraction data of 1 bank
        Args:
            ws_group_name
            bank_id:
            x_unit:
        Returns:
        3-tuple of numpy 1D array for X, Y and E
        """
        # check
        assert isinstance(bank_id, int) and bank_id > 0
        assert ws_group_name in self._braggDataDict, 'Workspace groups %s does not exist in controller.' % ws_group_name

        ws_name = '%s_bank%d' % (ws_group_name.split('_group')[0], bank_id)
        error_message = 'Bank %d is not found in group %s. Available bank IDs are %s.' % (
            bank_id, ws_group_name,  str(self._braggDataDict[ws_group_name][1]))
        assert ws_name in self._braggDataDict[ws_group_name][1], error_message

        # FIXME - It is quite messy here! Using dictionary or forming workspace name?
        # construct bank workspace name
        # ws_name = self._braggDataDict[ws_group_name][1][bank_id]
        assert AnalysisDataService.doesExist(ws_name), 'Workspace %s does not exist.' % ws_name

        # convert units if necessary
        bank_ws = AnalysisDataService.retrieve(ws_name)
        curr_unit = bank_ws.getAxis(0).getUnit().unitID()
        if curr_unit != x_unit:
            simpleapi.ConvertToHistogram(InputWorkspace=ws_name, OutputWorkspace=ws_name)
            simpleapi.ConvertUnits(InputWorkspace=ws_name, OutputWorkspace=ws_name,
                                       Target=x_unit, EMode='Elastic')

        # convert to point data for plotting
        simpleapi.ConvertToPointData(InputWorkspace=ws_name, OutputWorkspace=ws_name)

        # get workspace
        bank_ws = AnalysisDataService.retrieve(ws_name)

        return bank_ws.readX(0), bank_ws.readY(0), bank_ws.readE(0)

    def get_current_sq_name(self):
        """
        Get the (workspace) name of current S(Q)
        Returns:

        """
        return self._currSqWsName

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

    def get_gr_by_ws(self, gr_ws_name):
        """
        Parameters
        ----------
        gr_ws_name

        Returns
        -------

        """
        assert AnalysisDataService.doesExist(gr_ws_name), 'Workspace %s does not exist.' % gr_ws_name

        gr_ws = AnalysisDataService.retrieve(gr_ws_name)

        return gr_ws.readX(0), gr_ws.readY(0), gr_ws.readE(0)

    def get_sq(self, sq_name=None):
        """
        Get S(Q)
        Returns
        -------
        3-tuple of numpy array as Q, S(Q) and Sigma(Q)
        """
        # check
        assert isinstance(sq_name, str) or sq_name is None

        # set up default
        if sq_name is None:
            sq_name = self._currSqWsName

        assert AnalysisDataService.doesExist(sq_name), 'S(Q) matrix workspace %s does not exist.' \
                                                       '' % sq_name

        # access output workspace and return vector X, Y, E
        out_ws = AnalysisDataService.retrieve(sq_name)

        return out_ws.readX(0), out_ws.readY(0), out_ws.readE(0)

    def get_ws_data(self, ws_name):
        """

        Parameters
        ----------
        ws_name

        Returns
        -------

        """
        # convert to point data for plotting
        simpleapi.ConvertToPointData(InputWorkspace=ws_name, OutputWorkspace=ws_name)

        out_ws = AnalysisDataService.retrieve(ws_name)

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

    def load_gr(self, gr_file_name):
        """
        Load an ASCII file containing G(r)
        Args:
            gr_file_name:

        Returns:

        """
        # check
        assert isinstance(gr_file_name, str) and len(gr_file_name) > 0

        # load
        gr_ws_name = os.path.basename(gr_file_name).split('.')[0]
        simpleapi.LoadAscii(Filename=gr_file_name, OutputWorkspace=gr_ws_name, Unit='Empty')

        # check output
        if not AnalysisDataService.doesExist(gr_ws_name):
            return False, 'Unable to load file %s as target workspace %s cannot be found.' % (gr_ws_name,
                                                                                              gr_ws_name)

        return True, gr_ws_name

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
        sq_ws_name = os.path.basename(file_name).split('.')[0]
        print '[DB...BAT] Split file %s to workspace %s.' % (file_name, sq_ws_name)

        simpleapi.LoadAscii(Filename=file_name, OutputWorkspace=sq_ws_name, Unit='MomentumTransfer')
        assert AnalysisDataService.doesExist(sq_ws_name), 'Unable to load S(Q) file %s.' % file_name

        # TODO/FIXME : it is in fact S(Q)-1 in sq file.  So need to add 1 to the workspace
        out_ws = AnalysisDataService.retrieve(sq_ws_name)
        out_ws += 1

        # set to the current S(Q) workspace name
        self._currSqWsName = sq_ws_name
        self._sqIndexDict[self._currSqWsName] = 0

        # get range of Q from the loading
        sq_ws = AnalysisDataService.retrieve(sq_ws_name)
        q_min = sq_ws.readX(0)[0]
        q_max = sq_ws.readX(0)[-1]

        return sq_ws_name, q_min, q_max

    def split_to_single_bank(self, gss_ws_name):
        """
        Split a multiple-bank GSAS workspace to a set of single-spectrum MatrixWorkspace
        Parameters
        ----------
        gss_ws_name

        Returns
        -------
        Name of grouped workspace and list
        """
        # check
        assert isinstance(gss_ws_name, str)
        assert AnalysisDataService.doesExist(gss_ws_name)

        # get workspace
        gss_ws = AnalysisDataService.retrieve(gss_ws_name)

        ws_list = list()
        angle_list = list()

        if gss_ws.getNumberHistograms() == 1:
            # input is already a single-spectrum workspace
            ws_list.append(gss_ws_name)
        else:
            num_spec = gss_ws.getNumberHistograms()

            for i_ws in range(num_spec):
                # split this one to a single workspace
                out_ws_name = '%s_bank%d' % (gss_ws_name, i_ws+1)
                # also can use ExtractSpectra()
                simpleapi.CropWorkspace(InputWorkspace=gss_ws_name,
                                        OutputWorkspace=out_ws_name,
                                        StartWorkspaceIndex=i_ws, EndWorkspaceIndex=i_ws)
                assert AnalysisDataService.doesExist(out_ws_name)
                ws_list.append(out_ws_name)

            # END-FOR
        # END-IF

        # calculate bank angles
        for ws_name in ws_list:
            bank_angle = calculate_bank_angle(ws_name)
            angle_list.append(bank_angle)

        # group all the workspace
        ws_group_name = gss_ws_name + '_group'
        simpleapi.GroupWorkspaces(InputWorkspaces=ws_list,
                                  OutputWorkspace=ws_group_name)

        self._braggDataDict[ws_group_name] = (gss_ws_name, ws_list)

        return ws_group_name, ws_list, angle_list

    @staticmethod
    def save_ascii(ws_name, file_name):
        """

        Args:
            ws_name:
            file_name:

        Returns:

        """
        assert isinstance(ws_name, str)
        assert isinstance(file_name, str)
        simpleapi.SaveAscii(InputWorkspace=ws_name, Filename=file_name)

        return

    @staticmethod
    def write_gss_file(workspace, gss_file_name):
        """
        Write a MatrixWorkspace to a GSAS file
        Args:
            workspace:
            gss_file_name:

        Returns:

        """
        # check
        assert AnalysisDataService.doesExist(workspace)
        assert isinstance(gss_file_name, str)

        # write
        simpleapi.SaveGSS(InputWorkspace=workspace, Filename=gss_file_name,
                          Format='SLOG', Bank=1)

        return


def calculate_bank_angle(ws_name):
    """ Calculate bank's angle (2theta) focused detector
    """
    try:
        bank_ws = AnalysisDataService.retrieve(ws_name)
        instrument = bank_ws.getInstrument()
        det_pos = bank_ws.getDetector(0).getPos()
        sample_pos = instrument.getSample().getPos()
        source_pos = instrument.getSource().getPos()

        angle = (det_pos - sample_pos).angle(sample_pos - source_pos) * 180. / math.pi

    except KeyError:
        return None

    return angle
