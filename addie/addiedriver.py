from __future__ import (absolute_import, division, print_function)
from mantid.api import AnalysisDataService
import mantid.simpleapi as simpleapi
import os
import sys
import math
import numpy as np

# add a python path for local development
sys.path.append('/opt/mantid38/bin/')
sys.path.append('/Users/wzz/MantidBuild/debug-stable/bin/')


class AddieDriver(object):
    """
    Driver for addie application
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

    def calculate_gr(self, sq_ws_name, pdf_type, min_r, delta_r, max_r, min_q, max_q, pdf_filter, rho0):
        """ Calculate G(R)
        :param sq_ws_name: workspace name of S(q)
        :param pdf_type: type of PDF as G(r), g(r) and RDF(r)
        :param min_r: R_min
        :param delta_r: delta R
        :param max_r:
        :param min_q:
        :param max_q:
        :param pdf_filter: type of PDF filter
        :param rho0: average number density used for g(r) and RDF(r) conversions
        :return: string as G(r) workspace's name
        """
        # check
        assert isinstance(sq_ws_name, str) and AnalysisDataService.doesExist(sq_ws_name)
        assert isinstance(pdf_type, str) and len(pdf_type) > 0, \
            'PDF type is %s is not supported.' % str(pdf_type)
        assert min_r < max_r, 'Rmin must be less than Rmax (%f >= %f)' % (min_r, max_r)
        assert delta_r < (max_r - min_r), 'Must have more than one bin in G(r) (%f >= %f)' \
                                          '' % (delta_r, (max_r - min_r))

        assert min_q < max_q, 'Qmin must be less than Qmax (%f >= %f)' % (min_q, max_q)
        assert isinstance(pdf_filter, str) or pdf_filter is None, 'PDF filter must be a string or None.'
        assert isinstance(rho0, float) or rho0 is None, 'rho0 must be either None or a float but not a %s.' \
                                                        '' % str(type(rho0))

        # set to the current S(q) workspace name
        self._currSqWsName = sq_ws_name

        # set up the parameters for FourierTransform
        # output workspace
        prefix = 'G'
        if pdf_type.startswith('g'):
            prefix = 'g'
        elif pdf_type.startswith('R'):
            prefix = 'RDF'

        if self._currSqWsName in self._sqIndexDict:
            # for S(q) loaded from file
            ws_seq_index = self._sqIndexDict[self._currSqWsName]
            update_index = True
        else:
            # for S(q) calculated from IPython console
            ws_seq_index = 0
            update_index = False

        if pdf_filter is None:
            pdf_filter = False
        else:
            pdf_filter = True
            if pdf_filter != 'lorch':
                print('[WARNING] PDF filter {0} is not supported.'.format(pdf_filter))

        gr_ws_name = '%s(R)_%s_%d' % (prefix, self._currSqWsName, ws_seq_index)
        kwargs = {'OutputWorkspace': gr_ws_name,
                  'Qmin': min_q,
                  'Qmax': max_q,
                  'PDFType': pdf_type,
                  'DeltaR': delta_r,
                  'Rmax': max_r,
                  'Filter': pdf_filter}
        if rho0 is not None:
            kwargs['rho0'] = rho0

        # get the input unit
        sq_ws = AnalysisDataService.retrieve(self._currSqWsName)
        sofq_type = 'S(Q)'

        # do the FFT
        simpleapi.PDFFourierTransform(InputWorkspace=self._currSqWsName,
                                      InputSofQType=sofq_type,
                                      **kwargs)

        # check
        assert AnalysisDataService.doesExist(gr_ws_name), 'Failed to do Fourier Transform.'
        self._grWsNameDict[(min_q, max_q)] = gr_ws_name

        # update state variable
        if update_index:
            self._sqIndexDict[self._currSqWsName] += 1

        return gr_ws_name

    @staticmethod
    def clone_workspace(src_name, target_name):
        """clone workspace
        :param src_name:
        :param target_name:
        :return:
        """
        # check
        assert isinstance(src_name, str), 'blabla'
        assert isinstance(target_name, str), 'blabla'

        # check existence
        if AnalysisDataService.doesExist(src_name):
            simpleapi.CloneWorkspace(InputWorkspace=src_name, OutputWorkspace=target_name)
        else:
            raise RuntimeError('Workspace with name {0} does not exist in ADS. CloneWorkspace fails!'.format(src_name))

        return

    @staticmethod
    def delete_workspace(workspace_name, no_throw=False):
        """
        Delete a workspace from Mantid's AnalysisDataService
        Args:
            workspace_name: name of a workspace as a string instance
            no_throw: if True, then it won't throw any exception if the workspace does not exist in AnalysisDataService

        Returns: None

        """
        # check
        assert isinstance(workspace_name, str), \
            'Input workspace name must be a string, but not %s.' % str(type(workspace_name))

        # check whether the workspace exists
        does_exit = AnalysisDataService.doesExist(workspace_name)
        if does_exit:
            # delete
            simpleapi.DeleteWorkspace(Workspace=workspace_name)
        elif not no_throw:
            raise RuntimeError('Workspace %s does not exist.' % workspace_name)

        return

    @staticmethod
    def edit_matrix_workspace(sq_name, scale_factor, shift, edited_sq_name=None):
        """
        Edit the matrix workspace of S(Q) by scaling and shift
        :param sq_name: name of the SofQ workspace
        :param scale_factor:
        :param shift:
        :param edited_sq_name: workspace for the edited S(Q)
        :return:
        """
        # get the workspace
        if AnalysisDataService.doesExist(sq_name) is False:
            raise RuntimeError('S(Q) workspace {0} cannot be found in ADS.'.format(sq_name))

        if edited_sq_name is not None:
            simpleapi.CloneWorkspace(InputWorkspace=sq_name, OutputWorkspace=edited_sq_name)
            sq_ws = AnalysisDataService.retrieve(edited_sq_name)
        else:
            sq_ws = AnalysisDataService.retrieve(sq_name)

        # get the vector of Y
        sq_ws = sq_ws * scale_factor
        sq_ws = sq_ws + shift
        if sq_ws.name() != edited_sq_name:
            simpleapi.DeleteWorkspace(Workspace=edited_sq_name)
            simpleapi.RenameWorkspace(InputWorkspace=sq_ws, OutputWorkspace=edited_sq_name)

        assert sq_ws is not None, 'S(Q) workspace cannot be None.'
        print('[DB...BAT] S(Q) workspace that is edit is {0}'.format(sq_ws))

        return

    # RMCProfile format. The 1st column tells how many X,Y pairs,
    # the second is a comment line with information regarding the data
    # (title, multiplier for data, etc.), and then the X,Y pairs for G(r) or S(Q) data.

    @staticmethod
    def export_to_rmcprofile(ws_name, output_file_name, comment='', ws_index=0):
        """ Export a workspace 2D to a 2 column data for RMCProfile
        """
        # check inputs
        assert isinstance(ws_name, str), 'Workspace name {0} must be a string but not a {1}.'.format(ws_name,
                                                                                                     str(ws_name))
        assert isinstance(output_file_name, str), 'Output file name {0} must be a string but not a {1}.'.format(output_file_name,
                                                                                                                type(output_file_name))
        assert isinstance(comment, str), 'Comment {0} must be a string but not a {1}.'.format(comment, type(comment))
        assert isinstance(ws_index, int), 'Workspace index must be an integer but not a {1}.'.format(ws_index,
                                                                                                     type(ws_index))

        # convert to point data from histogram
        simpleapi.ConvertToPointData(InputWorkspace=ws_name, OutputWorkspace=ws_name)

        # get workspace for vecX and vecY
        if AnalysisDataService.doesExist(ws_name):
            workspace = AnalysisDataService.retrieve(ws_name)
        else:
            raise RuntimeError('Workspace {0} does not exist in ADS.'.format(ws_name))
        if not 0 <= ws_index < workspace.getNumberHistograms():
            raise RuntimeError('Workspace index {0} is out of range.'.format(ws_index))

        vec_x = workspace.readX(ws_index)
        vec_y = workspace.readY(ws_index)

        # write to buffer
        wbuf = ''
        wbuf += '{0}\n'.format(len(vec_x))
        wbuf += '{0}\n'.format(comment)
        for index in range(len(vec_x)):
            wbuf += ' {0} {1}\n'.format(vec_x[index], vec_y[index])

        # write to file
        try:
            ofile = open(output_file_name, 'w')
            ofile.write(wbuf)
            ofile.close()
        except IOError as io_err:
            raise RuntimeError(
                'Unable to export data to file {0} in RMCProfile format due to {1}.'.format(output_file_name, io_err))

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
        msg = 'Workspace groups {} does not exist in controller.'.format(ws_group_name)
        msg += 'Current existing are {}.'.format(self._braggDataDict.keys())
        assert ws_group_name in self._braggDataDict, msg

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
        """Get G(r)

        :param min_q:
        :param max_q:
        :return: 3-tuple for numpy.array
        """
        # check... find key in dictionary
        error_msg = 'R-range and delta R are not support. Current stored G(R) parameters' \
                    ' are {}.'.format(list(self._grWsNameDict.keys()))
        assert (min_q, max_q) in self._grWsNameDict, error_msg

        # get the workspace
        gr_ws_name = self._grWsNameDict[(min_q, max_q)]
        gr_ws = AnalysisDataService.retrieve(gr_ws_name)

        return gr_ws.readX(0), gr_ws.readY(0), gr_ws.readE(0)

    def get_sq(self, sq_name=None):
        """Get S(Q)
        :param sq_name:
        :return: 3-tuple of numpy array as Q, S(Q) and Sigma(Q)
        """
        # check
        assert isinstance(sq_name, str) or sq_name is None, 'Input S(Q) must either a string or None but not {0}.' \
                                                            ''.format(type(sq_name))

        # set up default
        if sq_name is None:
            sq_name = self._currSqWsName

        if not AnalysisDataService.doesExist(sq_name):
            raise RuntimeError('S(Q) matrix workspace {0} does not exist.'.format(sq_name))

        # access output workspace and return vector X, Y, E
        out_ws = AnalysisDataService.retrieve(sq_name)

        return out_ws.readX(0), out_ws.readY(0), out_ws.readE(0)

    @staticmethod
    def get_ws_data(ws_name):
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
    def get_ws_unit(ws_name):
        """
        Find out the unit of the workspace
        Parameters
        ----------
        ws_name

        Returns
        -------

        """
        # check
        assert isinstance(ws_name, str), 'Workspace name must be a string but not a %s.' % ws_name.__class__.__name__
        assert AnalysisDataService.doesExist(ws_name), 'Workspace %s does not exist.' % ws_name

        ws = AnalysisDataService.retrieve(ws_name)

        unit = ws.getAxis(0).getUnit().unitID()

        return unit

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
        if base_file_name.endswith('.gss') or base_file_name.endswith('.gsa') or base_file_name.endswith('.gda'):
            simpleapi.LoadGSS(Filename=file_name,
                              OutputWorkspace=gss_ws_name)
        elif base_file_name.endswith('.nxs'):
            simpleapi.LoadNexusProcessed(Filename=file_name, OutputWorkspace=gss_ws_name)
            simpleapi.ConvertUnits(InputWorkspace=gss_ws_name, OutputWorkspace=gss_ws_name, EMode='Elastic', Target='TOF')
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
        assert len(gr_file_name) > 0

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
        # generate S(Q) workspace name
        sq_ws_name = os.path.basename(file_name).split('.')[0]

        # call mantid LoadAscii
        ext = file_name.upper().split('.')[-1]
        if ext == 'NXS':
            simpleapi.LoadNexusProcessed(Filename=file_name, OutputWorkspace=sq_ws_name)
            simpleapi.ConvertUnits(InputWorkspace=sq_ws_name, OutputWorkspace=sq_ws_name, EMode='Elastic', Target='MomentumTransfer')
            simpleapi.ConvertToPointData(InputWorkspace=sq_ws_name, OutputWorkspace=sq_ws_name)  # TODO REMOVE THIS LINE
        elif ext == 'DAT' or ext == 'txt':
            simpleapi.LoadAscii(Filename=file_name, OutputWorkspace=sq_ws_name, Unit='MomentumTransfer')

        assert AnalysisDataService.doesExist(sq_ws_name), 'Unable to load S(Q) file %s.' % file_name

        # The S(Q) file is in fact S(Q)-1 in sq file.  So need to add 1 to the workspace
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

    def save_ascii(self, ws_name, file_name, gr_file_type, comment=''):
        """
        save ascii for G(r) or S(Q)
        Args:
            ws_name:
            file_name:
            gr_file_type: xye, csv, rmcprofile, dat
            comment: user comment to the file

        Returns:

        """
        assert isinstance(ws_name, str), 'blabla'
        assert isinstance(file_name, str), 'blabla'
        assert isinstance(gr_file_type, str), 'GofR file type {0} must be a supported string.'.format(gr_file_type)

        if gr_file_type == 'xye':
            simpleapi.SaveAscii(InputWorkspace=ws_name, Filename=file_name, Separator='Space')
        elif gr_file_type == 'csv':
            simpleapi.SaveAscii(InputWorkspace=ws_name, Filename=file_name, Separator='CSV')
        elif gr_file_type == 'rmcprofile' or gr_file_type == 'dat':
            self.export_to_rmcprofile(ws_name, file_name, comment=comment)
        elif gr_file_type == 'gr':
            simpleapi.SavePDFGui(InputWorkspace=ws_name, Filename=file_name)
        else:
            # non-supported type
            raise RuntimeError('G(r) or S(Q) file type {0} is not supported.'.format(gr_file_type))

        return

    @staticmethod
    def write_gss_file(ws_name_list, gss_file_name):
        """
        Write a MatrixWorkspace to a GSAS file
        Args:
            workspace:
            gss_file_name:

        Returns:

        """
        # check
        assert isinstance(ws_name_list, list) and len(ws_name_list) > 1, \
            'There must be at least 2 workspaces for conjoining operation.'
        assert isinstance(gss_file_name, str)

        # write with appending
        append_mode = False
        for i_ws, ws_name in enumerate(ws_name_list):
            simpleapi.SaveGSS(InputWorkspace=ws_name, Filename=gss_file_name,
                              Format='SLOG', Bank=1, Append=append_mode)
            append_mode = True
        # END-FOR

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
