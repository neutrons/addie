from __future__ import (absolute_import, division, print_function)
import numpy as np
import scipy.constants

# Constants
avogadro = scipy.constants.N_A
cm3_to_angstroms3 = 1e24
avogadro_term = avogadro / 1e24


def is_int(value):
    """Checks if `value` is an integer
    :param value: Input value to check if integer
    :type value: Any
    :return: If value is an integer
    :rtype: bool
    """

    is_number = True
    try:
        int(value)
    except ValueError:
        is_number = False

    return is_number


def is_float(value):
    """Checks if `value` is a float
    :param value: Input value to check if float
    :type value: Any
    :return: If value is an float
    :rtype: bool
    """

    is_number = True
    try:
        float(value)
    except ValueError:
        is_number = False

    return is_number


def is_number(value):
    """Checks if `value` is a float
    :param value: Input value to check if float
    :type value: Any
    :return: If value is an float
    :rtype: bool
    """
    return is_float(value)


def volume_of_cylinder(radius=np.NaN, height=np.NaN):
    """Computes volume of a cylinder
    :param radius: Radius of cylinder (in units of length)
    :type radius: float
    :param height: Height of cylinder (in units of length)
    :type height: float
    :return: Volume of the cylinder in (in units of :math:`length^{3}`)
    :rtype: float
    """
    return np.float(np.pi) * np.float(radius)**2 * np.float(height)


def volume_of_sphere(radius=np.NaN):
    """Computes volume of a sphere
    :param radius: Radius of sphere (in units of length)
    :type radius: float
    :return: Volume of the sphere in (in units of :math:`length^{3}`)
    :rtype: float
    """
    return (4. * np.pi * np.float(radius)**3 / np.float(3))


def volume_of_hollow_cylinder(inner_radius=np.NaN, outer_radius=np.NaN, height=np.NaN):
    """Computes volume of a hollow cylinder
    :param inner_radius: Inner radius of cylinder (in units of length)
    :type inner_radius: float
    :param outer_radius: Outer radius of cylinder (in units of length)
    :type outer_radius: float
    :param height: Height of cylinder (in units of length)
    :type height: float
    :return: Volume of the cylinder in (in units of :math:`length^{3}`)
    :rtype: float
    """
    inner_cylinder = volume_of_cylinder(radius=inner_radius, height=height)
    outer_cylinder = volume_of_cylinder(radius=outer_radius, height=height)
    return outer_cylinder - inner_cylinder


def mass_density2number_density(mass_density, natoms, molecular_mass):
    """Converts from mass_density (:math:`g/cm^{3}`) to number density (atoms/:math:`\\AA^{3}`)
    :param mass_density: mass density in (:math:`g/cm^{3}`)
    :type mass_density: float
    :param natoms: total number of atoms
    :type natoms: float
    :param molecular_mass: molecular mass in (:math:`g/mol`)
    :type molecular_mass: float
    :return: number density in (atoms/:math:`\\AA^{3}`)
    :rtype: float
    """
    number_density = mass_density * avogadro_term * natoms / molecular_mass
    number_density = "{:.5}".format(number_density)
    return number_density


def number_density2mass_density(number_density, natoms, molecular_mass):
    """Converts from number density (atoms/:math:`\\AA^{3}`) to mass_density (:math:`g/cm^{3}`)
    :param number_density: number density in (atoms/:math:`\\AA^{3}`)
    :type number_density: float
    :param natoms: total number of atoms
    :type natoms: float
    :param molecular_mass: molecular mass in (:math:`g/mol`)
    :type molecular_mass: float
    :return: mass density in (:math:`g/cm^{3}`)
    :rtype: float
    """
    mass_density = number_density * molecular_mass / natoms / avogadro_term
    mass_density = "{:.5}".format(mass_density)
    return mass_density
