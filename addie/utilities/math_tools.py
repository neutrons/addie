from __future__ import (absolute_import, division, print_function)
import numpy as np

def is_int(value):

    is_number = True
    try:
        int(value)
    except ValueError:
        is_number = False

    return is_number

def is_float(value):

    is_number = True
    try:
        float(value)
    except ValueError:
        is_number = False

    return is_number

def is_number(value):
    return is_float(value)

def volume_of_cylinder(radius=np.NaN, height=np.NaN):
    return np.float(np.pi) * np.float(radius)**2 * np.float(height)

def volume_of_sphere(radius=np.NaN):
    return (4. * np.pi * np.float(radius)**3 / np.float(3))

def volume_of_hollow_cylinder(inner_radius=np.NaN, outer_radius=np.NaN, height=np.NaN):
    inner_cylinder = volume_of_cylinder(radius=inner_radius, height=height)
    outer_cylinder = volume_of_cylinder(radius=outer_radius, height=height)
    return outer_cylinder - inner_cylinder
