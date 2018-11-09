from collections import OrderedDict
import copy
from os.path import expanduser
import os

user_home = expanduser("~")
CONFIG_FILE = os.path.join(user_home, '.addie_config.cfg')

column_default_width = 90

h_index = {'h1': None,
               'h2': None,
               'h3': None}

base_dict = {'ui': None,
                      'name': "Title",
                      'children': None,
                      'h_index': copy.deepcopy(h_index),
                      }

tree_dict = OrderedDict()
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

sample_children_1['sample_packing_fraction'] = copy.deepcopy(base_dict)
sample_children_1['sample_packing_fraction']['name'] = "Packing Fraction"

sample_children_2 = OrderedDict()
sample_children_2['sample_geometry_shape'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_shape']['name'] = "Shape"

sample_children_2['sample_geometry_radius'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_radius']['name'] = "Radius"

sample_children_2['sample_geometry_Height'] = copy.deepcopy(base_dict)
sample_children_2['sample_geometry_Height']['name'] = "Height"

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

vanadium_children_1['vanadium_packing_fraction'] = copy.deepcopy(base_dict)
vanadium_children_1['vanadium_packing_fraction']['name'] = "Packing Fraction"

vanadium_children_2 = OrderedDict()
vanadium_children_2['vanadium_geometry_shape'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_shape']['name'] = 'Shape'

vanadium_children_2['vanadium_geometry_radius'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_radius']['name'] = 'Radius'

vanadium_children_2['vanadium_geometry_Height'] = copy.deepcopy(base_dict)
vanadium_children_2['vanadium_geometry_Height']['name'] = 'Height'

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
tree_dict['vanadium']['name'] = 'Vanadium'
tree_dict['vanadium']['children'] = vanadium_children_1