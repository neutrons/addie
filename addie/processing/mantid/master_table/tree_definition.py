from collections import OrderedDict
import copy
from os.path import expanduser
import os
import numpy as np

user_home = expanduser("~")
CONFIG_FILE = os.path.join(user_home, '.addie_config.cfg')

COLUMNS_IDENTICAL_VALUES_COLOR = [0, 255, 255] # cyan
COLUMNS_DIFFERENT_VALUES_COLOR = [255, 255, 255] # white

COLUMN_DEFAULT_WIDTH = 90
COLUMN_DEFAULT_HEIGHT = 120
CONFIG_BUTTON_HEIGHT = 20
CONFIG_BUTTON_WIDTH = 30

h3_COLUMNS_WIDTH = [90,  #activate #0
                    250,  #title #1
                    150,  #runs  #sample #2
                    90,  #background runs #3
                    90,  #background background #4
                    150,  #chemical formula #5
                    150,  #mass density #6
                    120,  #packing fraction #7
                    150,  #shape #8
                    200, # geometry dimensions #9
                    150, 200, 150,  #correction #10, 11, 12
                    200, # Resonance #13
                    90,  # runs  #normalization #14
                    90,  # background runs #15
                    90,  # background background #16
                    150,  #chemical formula #17
                    150,  # mass density #18
                    120,  # packing fraction #19
                    150,  # shape #20
                    200, # geometry dimensions #21
                    150, 200, 150,  # correction #22, 23, 24
                    150, # key/value pairs #25
                    350, # self-scattering level #26
                    ]

h2_COLUMNS_WIDTH = [h3_COLUMNS_WIDTH[0], #0
                    h3_COLUMNS_WIDTH[1], #1
                    h3_COLUMNS_WIDTH[2], #2
                    h3_COLUMNS_WIDTH[3] + h3_COLUMNS_WIDTH[4], #3
                    h3_COLUMNS_WIDTH[5], #4
                    h3_COLUMNS_WIDTH[6], #5
                    h3_COLUMNS_WIDTH[7], #6
                    h3_COLUMNS_WIDTH[8]+h3_COLUMNS_WIDTH[9], #7
                    h3_COLUMNS_WIDTH[10], #8
                    h3_COLUMNS_WIDTH[11], #9
                    h3_COLUMNS_WIDTH[12], #10, resonance
                    h3_COLUMNS_WIDTH[13], #11
                    h3_COLUMNS_WIDTH[14], #12
                    h3_COLUMNS_WIDTH[15]+h3_COLUMNS_WIDTH[16], #13
                    h3_COLUMNS_WIDTH[17], #14
                    h3_COLUMNS_WIDTH[18], #15
                    h3_COLUMNS_WIDTH[19], #16
                    h3_COLUMNS_WIDTH[20]+h3_COLUMNS_WIDTH[21], #17
                    h3_COLUMNS_WIDTH[22], #18
                    h3_COLUMNS_WIDTH[23], #19
                    h3_COLUMNS_WIDTH[24], #20
                    h3_COLUMNS_WIDTH[25], #21
                    h3_COLUMNS_WIDTH[26], #22
                    ]

h1_COLUMNS_WIDTH = [h3_COLUMNS_WIDTH[0],
                    h3_COLUMNS_WIDTH[1],
                    np.sum(h3_COLUMNS_WIDTH[2:14]),
                    np.sum(h3_COLUMNS_WIDTH[14:24]),
                    h3_COLUMNS_WIDTH[25],
                    h3_COLUMNS_WIDTH[26],
                    ]
INDEX_OF_COLUMNS_SEARCHABLE = [1,2,3,4,7,14,15,16,19]
INDEX_OF_SPECIAL_COLUMNS_SEARCHABLE = [5, 6, 17, 18, 25]   # where we need to look inside the widget_cell, not only item

INDEX_OF_COLUMNS_SHAPE = [8, 20]
INDEX_OF_ABS_CORRECTION = [10, 22]
INDEX_OF_MULTI_SCATTERING_CORRECTION = [11, 23]
INDEX_OF_INELASTIC_CORRECTION = [12, 24]

INDEX_OF_COLUMNS_WITH_COMBOBOX = [INDEX_OF_COLUMNS_SHAPE[0],
                                  INDEX_OF_ABS_CORRECTION[0],
                                  INDEX_OF_MULTI_SCATTERING_CORRECTION[0],
                                  INDEX_OF_INELASTIC_CORRECTION[0],
                                  INDEX_OF_COLUMNS_SHAPE[1],
                                  INDEX_OF_ABS_CORRECTION[1],
                                  INDEX_OF_MULTI_SCATTERING_CORRECTION[1],
                                  INDEX_OF_INELASTIC_CORRECTION[1],
                                  ]

INDEX_SAMPLE_START = 1
INDEX_NORMALIZATION_START = 14
INDEX_OF_COLUMNS_WITH_CHECKBOX = [0]
INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA = [5, 17]
INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS = [9, 21]
INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS = [13]
INDEX_OF_COLUMNS_WITH_MASS_DENSITY = [6, 18]
INDEX_OF_COLUMNS_WITH_ALIGN_AND_FOCUS_ARGS = [25]
INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS = [26]
INDEX_OF_COLUMNS_WITH_ITEMS = INDEX_OF_COLUMNS_SEARCHABLE

LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING = [3,  # sample background runs
                                                4,  # sample background background
                                                5,  # sample chemical formula
                                                6,  # sample mass density
                                                7,  # sample packing fraction
                                                8, 9,  # sample geometry shape and dimensions
                                                10, 11, 12,  # Sample correction
                                                13, #resonance
                                                14,  # normalization  runs
                                                15,  # normalization background runs
                                                16,  # normalization background background
                                                17,  # normalization chemical formula
                                                18,  # normalization mass density
                                                19,  # normalization packing fraction
                                                20, 21,  # normalization geometry shape and dimensions
                                                22, 23, 24,  # normalization correction
                                                25,  # Align and Focus Args
                                                26, #Self scattering levels
                                                ]

SAMPLE_FIRST_COLUMN = 2
NORMALIZATION_FIRST_COLUMN = 14

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
sample_children_1['sample_material']['name'] = "Chemical Formula"

sample_children_1['sample_mass_density'] = copy.deepcopy(base_dict)
sample_children_1['sample_mass_density']['name'] = "Mass Density"

sample_children_1['sample_packing_fraction'] = copy.deepcopy(base_dict)
sample_children_1['sample_packing_fraction']['name'] = "Packing Fraction"

sample_children_2 = OrderedDict()
sample_children_2['sample_geometry_shape'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_shape']['name'] = "Shape"

sample_children_2['sample_geometry_dimensions'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_dimensions']['name'] = "Dimensions (cm)"

sample_children_1['sample_geometry'] = copy.deepcopy(base_dict)
sample_children_1['sample_geometry']['name'] = "Geometry"
sample_children_1['sample_geometry']['children'] = sample_children_2

sample_children_1['sample_absolute_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_absolute_correction']['name'] = "Abs. Correction"

sample_children_1['sample_multi_scattering_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_multi_scattering_correction']['name'] = 'Multi Scattering Correction'

sample_children_1['sample_inelastic_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_inelastic_correction']['name'] = 'Inelastic Correction'

sample_children_1['sample_resonance_correction'] = copy.deepcopy(base_dict)
sample_children_1['sample_resonance_correction']['name'] = 'Resonance Abs. Correction'

sample_children_2 = OrderedDict()
sample_children_2['sample_resonance_'] = copy.deepcopy(base_dict)
sample_children_2['sample_resonance_']['name'] = "Angstrom or eV"
sample_children_1['sample_resonance_correction']['children'] = sample_children_2

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
vanadium_children_1['vanadium_material']['name'] = "Chemical Formula"

vanadium_children_1['vanadium_mass_density'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_mass_density']['name'] = "Mass Density"

vanadium_children_1['vanadium_packing_fraction'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_packing_fraction']['name'] = "Packing Fraction"

vanadium_children_2 = OrderedDict()
vanadium_children_2['vanadium_geometry_shape'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_shape']['name'] = 'Shape'

vanadium_children_2['vanadium_geometry_dimensions'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_dimensions']['name'] = 'Dimensions (cm)'

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

tree_dict['align_and_focus_args'] = copy.deepcopy(base_dict)
tree_dict['align_and_focus_args']['name'] = 'Align and Focus Args.'

tree_dict['self_scattering_level'] = copy.deepcopy(base_dict)
tree_dict['self_scattering_level']['name'] = 'Self-Scattering Level'

LIST_SEARCH_CRITERIA = {'nom': ['Chemical Formula',
                                'Title',
                                'Sample Env. Device',
                                ],
                        'pg3': [''],
                        }

TREE_DICT = tree_dict
