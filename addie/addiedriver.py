from __future__ import (absolute_import, division, print_function)
from mantid.api import AnalysisDataService
import mantid.simpleapi as simpleapi

import os
import addie.utilities


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

    def calculate_sqAlt(self, ws_name, outputType):
        if outputType == 'S(Q)':  # don't do anything
            return ws_name
        elif outputType == 'Q[S(Q)-1]':
            outputType = 'F(Q)'
        else:
            # PDConvertReciprocalSpace doesn't currently know how to convert to
            # S(Q)-1
            raise ValueError(
                'Do not know how to convert to {}'.format(outputType))

        outputName = '__{}Alt'.format(ws_name)  # should be hidden
        simpleapi.PDConvertReciprocalSpace(
            InputWorkspace=ws_name,
            OutputWorkspace=outputName,
            From='S(Q)',
            To=outputType)
        return outputName

    def calculate_gr(
            self,
            sq_ws_name,
            pdf_type,
            min_r,
            delta_r,
            max_r,
            min_q,
            max_q,
            pdf_filter,
            rho0):
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
        assert isinstance(
            sq_ws_name,
            str) and AnalysisDataService.doesExist(sq_ws_name)
        assert isinstance(pdf_type, str) and len(pdf_type) > 0, \
            'PDF type is %s is not supported.' % str(pdf_type)
        assert min_r < max_r, 'Rmin must be less than Rmax (%f >= %f)' % (
            min_r, max_r)
        assert delta_r < (max_r - min_r), 'Must have more than one bin in G(r) (%f >= %f)' \
                                          '' % (delta_r, (max_r - min_r))

        assert min_q < max_q, 'Qmin must be less than Qmax (%f >= %f)' % (
            min_q, max_q)
        assert isinstance(
            pdf_filter, str) or pdf_filter is None, 'PDF filter must be a string or None.'

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
                print(
                    '[WARNING] PDF filter {0} is not supported.'.format(pdf_filter))

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

        # Print warning about using G(r) and rho0
        if 'rho0' in kwargs and pdf_type == "G(r)":
            print("WARNING: Modifying the density does not affect G(r) function")

        # get the input unit
        sofq_type = 'S(Q)'

        # do the FFT
        simpleapi.PDFFourierTransform(InputWorkspace=self._currSqWsName,
                                      InputSofQType=sofq_type,
                                      **kwargs)

        # check
        assert AnalysisDataService.doesExist(
            gr_ws_name), 'Failed to do Fourier Transform.'
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
            simpleapi.CloneWorkspace(
                InputWorkspace=src_name,
                OutputWorkspace=target_name)
        else:
            raise RuntimeError(
                'Workspace with name {0} does not exist in ADS. CloneWorkspace fails!'.format(src_name))

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
    def edit_matrix_workspace(
            sq_name,
            scale_factor,
            shift,
            edited_sq_name=None):
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
            raise RuntimeError(
                'S(Q) workspace {0} cannot be found in ADS.'.format(sq_name))

        if edited_sq_name is not None:
            simpleapi.CloneWorkspace(
                InputWorkspace=sq_name,
                OutputWorkspace=edited_sq_name)
            sq_ws = AnalysisDataService.retrieve(edited_sq_name)
        else:
            sq_ws = AnalysisDataService.retrieve(sq_name)

        # get the vector of Y
        sq_ws = sq_ws * scale_factor
        sq_ws = sq_ws + shift
        if sq_ws.name() != edited_sq_name:
            simpleapi.DeleteWorkspace(Workspace=edited_sq_name)
            simpleapi.RenameWorkspace(
                InputWorkspace=sq_ws,
                OutputWorkspace=edited_sq_name)

        assert sq_ws is not None, 'S(Q) workspace cannot be None.'
        print('[DB...BAT] S(Q) workspace that is edit is {0}'.format(sq_ws))

    # RMCProfile format. The 1st column tells how many X,Y pairs,
    # the second is a comment line with information regarding the data
    # (title, multiplier for data, etc.), and then the X,Y pairs for G(r) or S(Q) data.

    @staticmethod
    def export_to_rmcprofile(
            ws_name,
            output_file_name,
            comment='',
            ws_index=0):
        """ Export a workspace 2D to a 2 column data for RMCProfile
        """
        # check inputs
        assert isinstance(
            ws_name, str), 'Workspace name {0} must be a string but not a {1}.'.format(
            ws_name, str(ws_name))
        assert isinstance(
            output_file_name, str), 'Output file name {0} must be a string but not a {1}.'.format(
            output_file_name, type(output_file_name))
        assert isinstance(
            comment, str), 'Comment {0} must be a string but not a {1}.'.format(
            comment, type(comment))
        assert isinstance(
            ws_index, int), 'Workspace index must be an integer but not a {0}.'.format(
            type(ws_index))

        # # convert to point data from histogram
        # simpleapi.ConvertToPointData(
        #     InputWorkspace=ws_name,
        #     OutputWorkspace=ws_name)

        # get workspace for vecX and vecY
        if AnalysisDataService.doesExist(ws_name):
            workspace = AnalysisDataService.retrieve(ws_name)
        else:
            raise RuntimeError(
                'Workspace {0} does not exist in ADS.'.format(ws_name))
        if not 0 <= ws_index < workspace.getNumberHistograms():
            raise RuntimeError(
                'Workspace index {0} is out of range.'.format(ws_index))

        vec_x = workspace.readX(ws_index)[:-1]
        vec_y = workspace.readY(ws_index)

        # write to buffer
        wbuf = ''
        wbuf += '{0}\n'.format(len(vec_x))
        wbuf += '{0}\n'.format(comment)
        for index in range(len(vec_x)):
            wbuf += '{0:10.3F}{1:15.5F}\n'.format(vec_x[index], vec_y[index])

        # write to file
        try:
            ofile = open(output_file_name, 'w')
            ofile.write(wbuf)
            ofile.close()
        except IOError as io_err:
            msg = 'Unable to export data to file {0} in RMCProfile format due to {1}.'
            msg = msg.format(output_file_name, io_err)
            raise RuntimeError(msg)

    def get_bank_numbers(self, ws_name):
        '''Returns the list of spectrum numbers in the workspace'''
        wksp = addie.utilities.workspaces.get_ws(ws_name)
        banks = [wksp.getSpectrum(i).getSpectrumNo()
                 for i in range(wksp.getNumberHistograms())]
        return banks

    def convert_bragg_data(self, ws_name, x_unit):
        wksp = addie.utilities.workspaces.get_ws(ws_name)
        curr_unit = wksp.getAxis(0).getUnit().unitID()
        if curr_unit != x_unit:
            simpleapi.ConvertUnits(
                InputWorkspace=ws_name,
                OutputWorkspace=ws_name,
                Target=x_unit,
                EMode='Elastic')

    def get_bragg_data(self, ws_name, wkspindex, x_unit):
        """ Get Bragg diffraction data of 1 bank
        """
        # check
        assert isinstance(wkspindex, int) and wkspindex >= 0
        bank_ws = addie.utilities.workspaces.get_ws(ws_name)

        # convert units if necessary
        curr_unit = bank_ws.getAxis(0).getUnit().unitID()
        if curr_unit != x_unit:
            simpleapi.ConvertToHistogram(
                InputWorkspace=ws_name, OutputWorkspace=ws_name)
            simpleapi.ConvertUnits(
                InputWorkspace=ws_name,
                OutputWorkspace=ws_name,
                Target=x_unit,
                EMode='Elastic')

        return addie.utilities.workspaces.get_ws_data(ws_name, wkspindex)

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

        return addie.utilities.workspaces.get_ws_data(gr_ws_name)

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
            raise RuntimeError(
                'S(Q) matrix workspace {0} does not exist.'.format(sq_name))

        return addie.utilities.workspaces.get_ws_data(sq_name)

    def load_gr(self, gr_file_name):
        """
        Load an ASCII file containing G(r)
        """
        # check
        assert len(gr_file_name) > 0

        # load
        gr_ws_name = os.path.basename(gr_file_name).split('.')[0]
        simpleapi.LoadAscii(
            Filename=gr_file_name,
            OutputWorkspace=gr_ws_name,
            Unit='Empty')

        # check output
        if not AnalysisDataService.doesExist(gr_ws_name):
            return False, 'Unable to load file %s as target workspace %s cannot be found.' % (
                gr_ws_name, gr_ws_name)

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
            simpleapi.LoadNexusProcessed(
                Filename=file_name, OutputWorkspace=sq_ws_name)
            simpleapi.ConvertUnits(
                InputWorkspace=sq_ws_name,
                OutputWorkspace=sq_ws_name,
                EMode='Elastic',
                Target='MomentumTransfer')
            simpleapi.ConvertToPointData(
                InputWorkspace=sq_ws_name,
                OutputWorkspace=sq_ws_name)  # TODO REMOVE THIS LINE
        elif ext == 'DAT' or ext == 'txt':
            try:
                simpleapi.LoadAscii(
                    Filename=file_name,
                    OutputWorkspace=sq_ws_name,
                    Unit='MomentumTransfer')
            except RuntimeError:
                sq_ws_name, q_min, q_max = "InvalidInput", 0, 0
                return sq_ws_name, q_min, q_max
            # The S(Q) file is in fact S(Q)-1 in sq file.  So need to add 1 to
            # the workspace
            out_ws = AnalysisDataService.retrieve(sq_ws_name)
            out_ws += 1

        assert AnalysisDataService.doesExist(
            sq_ws_name), 'Unable to load S(Q) file %s.' % file_name

        # set to the current S(Q) workspace name
        self._currSqWsName = sq_ws_name
        self._sqIndexDict[self._currSqWsName] = 0

        # get range of Q from the loading
        sq_ws = AnalysisDataService.retrieve(sq_ws_name)
        q_min = sq_ws.readX(0)[0]
        q_max = sq_ws.readX(0)[-1]

        return sq_ws_name, q_min, q_max

    def save_ascii(self, ws_name, file_name, filetype, comment=''):
        """
        save ascii for G(r) or S(Q)
        Args:
            ws_name:
            file_name:
            filetype: xye, csv, rmcprofile, dat
            comment: user comment to the file

        Returns:

        """
        assert isinstance(
            filetype, str), 'GofR file type {0} must be a supported string.'.format(filetype)

        if filetype == 'xye' or filetype == 'gr':
            x_val = simpleapi.mtd[ws_name].readX(0)[:-1]
            y_val = simpleapi.mtd[ws_name].readY(0)
            e_val = simpleapi.mtd[ws_name].readE(0)

            file_out = open(file_name, "w")
            for i, item in enumerate(x_val):
                file_out.write("{0:10.3F}{1:15.5F}{2:15.5F}\n".format(item,
                                                                      y_val[i],
                                                                      e_val[i]))
            file_out.close()
        elif filetype == 'csv':
            x_val = simpleapi.mtd[ws_name].readX(0)[:-1]
            y_val = simpleapi.mtd[ws_name].readY(0)
            e_val = simpleapi.mtd[ws_name].readE(0)

            file_out = open(file_name, "w")
            for i, item in enumerate(x_val):
                file_out.write("{0:10.3F},{1:15.5F},{2:15.5F}\n".format(item,
                                                                        y_val[i],
                                                                        e_val[i]))
            file_out.close()
        elif filetype == 'rmcprofile' or filetype == 'dat':
            self.export_to_rmcprofile(ws_name, file_name, comment=comment)
        elif filetype == 'sq':
            simpleapi.SaveAscii(
                InputWorkspace=ws_name,
                Filename=file_name,
                Separator='Space')
        else:
            # non-supported type
            raise RuntimeError(
                'G(r) or S(Q) file type "{0}" is not supported.'.format(filetype))

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
