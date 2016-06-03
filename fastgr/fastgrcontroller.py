def load_gsas_file(gsa_file_name):
    """
    """
    api.LoadGSS(OutputWorkspace=out_ws_name)

    for ibank in xrange(6):
        api.ExtractSpectra()
        # or api.CropWorkspace()

    # END-FOR

    return


def conjoin_banks():
    """ Conjoin all 6 single banks
    """
    api.ConjoinWorkspaces()
