from collections import OrderedDict
import copy
from os.path import expanduser
import os
import numpy as np

user_home = expanduser("~")
CONFIG_FILE = os.path.join(user_home, '.addie_config.cfg')

column_default_width = 90
COLUMN_DEFAULT_HEIGHT = 50

h3_COLUMNS_WIDTH = [90,  #activate
                    150,  #title
                    90,  #runs  #sample
                    90,  #background runs
                    90,  #background background
                    90,  #material
                    120,  #mass density
                    120,  #packing fraction
                    90,  #shape
                    50, 50, 50,  #geometry dimensions
                    150, 150, 150,  #correction
                    90,  # runs  #normalization
                    90,  # background runs
                    90,  # background background
                    90,  # material
                    120,  # mass density
                    120,  # packing fraction
                    90,  # shape
                    50, 50, 50,  # geometry dimensions
                    150, 150, 150,  # correction
                    50, 50, # grouping
                    ]

h2_COLUMNS_WIDTH = [h3_COLUMNS_WIDTH[0],
                    h3_COLUMNS_WIDTH[1],
                    h3_COLUMNS_WIDTH[2],
                    h3_COLUMNS_WIDTH[3] + h3_COLUMNS_WIDTH[4],
                    h3_COLUMNS_WIDTH[5],
                    h3_COLUMNS_WIDTH[6],
                    h3_COLUMNS_WIDTH[7],
                    h3_COLUMNS_WIDTH[8]+h3_COLUMNS_WIDTH[9]+h3_COLUMNS_WIDTH[10]+h3_COLUMNS_WIDTH[11],
                    h3_COLUMNS_WIDTH[12],
                    h3_COLUMNS_WIDTH[13],
                    h3_COLUMNS_WIDTH[14],
                    h3_COLUMNS_WIDTH[15],
                    h3_COLUMNS_WIDTH[16]+h3_COLUMNS_WIDTH[17],
                    h3_COLUMNS_WIDTH[18],
                    h3_COLUMNS_WIDTH[19],
                    h3_COLUMNS_WIDTH[20],
                    h3_COLUMNS_WIDTH[21]+h3_COLUMNS_WIDTH[22]+h3_COLUMNS_WIDTH[23]+h3_COLUMNS_WIDTH[24],
                    h3_COLUMNS_WIDTH[25],
                    h3_COLUMNS_WIDTH[26],
                    h3_COLUMNS_WIDTH[27],
                    h3_COLUMNS_WIDTH[28],
                    h3_COLUMNS_WIDTH[29]]

h1_COLUMNS_WIDTH = [h3_COLUMNS_WIDTH[0],
                    h3_COLUMNS_WIDTH[1],
                    np.sum(h3_COLUMNS_WIDTH[2:15]),
                    np.sum(h3_COLUMNS_WIDTH[15:28]),
                    h3_COLUMNS_WIDTH[28],
                    h3_COLUMNS_WIDTH[29]]

INDEX_OF_COLUMNS_SEARCHABLE = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 15, 16, 17, 18, 19, 20, 22, 23, 24]

INDEX_OF_COLUMNS_WITH_COMBOBOX = [8, 12, 13, 14, 21, 25, 26, 27, ]

sample_first_column = 2
normalization_first_column = 15

h_index = {'h1': None,
           'h2': None,
           'h3': None}

base_dict = {'ui': None,
             'name': "",
             'children': None,
             'h_index': copy.deepcopy(h_index),
             }

tree_dict = OrderedDict()

tree_dict['activate'] = copy.deepcopy(base_dict)
tree_dict['activate']['name'] = 'Activate'

tree_dict['title'] = copy.deepcopy(base_dict)
tree_dict['title']['name'] = "Title"

sample_children_1 = OrderedDict()
sample_children_1['sample_runs'] = copy.deepcopy(base_dict)
sample_children_1['sample_runs']['name'] = "Runs"

sample_children_2 = OrderedDict()
sample_children_2['sample_background_runs'] = copy.deepcopy(base_dict)
sample_children_2['sample_background_runs']['name'] = "Runs"

sample_children_2['sample_background_background'] = copy.deepcopy(base_dict)
sample_children_2['sample_background_background']['name'] = "Background"

sample_children_1['sample_background'] = copy.deepcopy(base_dict)
sample_children_1['sample_background']['name'] = "Background"
sample_children_1['sample_background']['children'] = sample_children_2

sample_children_1['sample_material'] = copy.deepcopy(base_dict)
sample_children_1['sample_material']['name'] = "Material"

sample_children_1['sample_mass_density'] = copy.deepcopy(base_dict)
sample_children_1['sample_mass_density']['name'] = "Mass Density"

sample_children_1['sample_packing_fraction'] = copy.deepcopy(base_dict)
sample_children_1['sample_packing_fraction']['name'] = "Packing Fraction"

sample_children_2 = OrderedDict()
sample_children_2['sample_geometry_shape'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_shape']['name'] = "Shape"

sample_children_2['sample_geometry_radius'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_radius']['name'] = "Radius (cm)"

sample_children_2['sample_geometry_radius2'] = copy.deepcopy(base_dict)

sample_children_2['sample_geometry_Height'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_Height']['name'] = "Height (cm)"

sample_children_1['sample_geometry'] = copy.deepcopy(base_dict)
sample_children_1['sample_geometry']['name'] = "Geometry"
sample_children_1['sample_geometry']['children'] = sample_children_2

sample_children_1['sample_absolute_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_absolute_correction']['name'] = "Abs. Correction"

sample_children_1['sample_multi_scattering_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_multi_scattering_correction']['name'] = 'Multi Scattering Correction'

sample_children_1['sample_inelastic_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_inelastic_correction']['name'] = 'Inelastic Correction'

tree_dict['sample'] = copy.deepcopy(base_dict)
tree_dict['sample']['name'] = 'Sample'
tree_dict['sample']['children'] = sample_children_1

vanadium_children_1 = OrderedDict()
vanadium_children_1['vanadium_runs'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_runs']['name'] = "Runs"

vanadium_children_2 = OrderedDict()
vanadium_children_2['vanadium_background_runs'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_background_runs']['name'] = "Runs"

vanadium_children_2['vanadium_background_background'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_background_background']['name'] = "Background"

vanadium_children_1['vanadium_background'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_background']['name'] = "Background"
vanadium_children_1['vanadium_background']['children'] = vanadium_children_2

vanadium_children_1['vanadium_material'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_material']['name'] = "Materials"

vanadium_children_1['vanadium_mass_density'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_mass_density']['name'] = "Mass Density"

vanadium_children_1['vanadium_packing_fraction'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_packing_fraction']['name'] = "Packing Fraction"

vanadium_children_2 = OrderedDict()
vanadium_children_2['vanadium_geometry_shape'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_shape']['name'] = 'Shape'

vanadium_children_2['vanadium_geometry_radius'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_radius']['name'] = 'Radius (cm)'

vanadium_children_2['vanadium_geometry_radius2'] = copy.deepcopy(base_dict)

vanadium_children_2['vanadium_geometry_Height'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_Height']['name'] = 'Height (cm)'

vanadium_children_1['vanadium_geometry'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_geometry']['name'] = 'Geometry'
vanadium_children_1['vanadium_geometry']['children'] = vanadium_children_2

vanadium_children_1['vanadium_absolute_correction'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_absolute_correction']['name'] = "Abs. Correction"

vanadium_children_1['vanadium_multi_scattering_correction'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_multi_scattering_correction']['name'] = 'Multi Scattering Correction'

vanadium_children_1['vanadium_inelastic_correction'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_inelastic_correction']['name'] = "Inelastic Correction"

tree_dict['vanadium'] = copy.deepcopy(base_dict)
tree_dict['vanadium']['name'] = 'Normalization'
tree_dict['vanadium']['children'] = vanadium_children_1

tree_dict['input_grouping'] = copy.deepcopy(base_dict)
tree_dict['input_grouping']['name'] = "Input Grouping"

tree_dict['output_grouping'] = copy.deepcopy(base_dict)
tree_dict['output_grouping']['name'] = "Output Grouping"
