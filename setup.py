import os
from setuptools import setup, find_packages
import versioneer  # https://github.com/warner/python-versioneer

# ==============================================================================
# Constants
# ==============================================================================
THIS_DIR = os.path.dirname(__file__)

# ==============================================================================
# Package requirements helper
# ==============================================================================


def read_requirements_from_file(filepath):
    '''Read a list of requirements from the given file and split into a
    list of strings. It is assumed that the file is a flat
    list with one requirement per line.
    :param filepath: Path to the file to read
    :return: A list of strings containing the requirements
    '''
    with open(filepath, 'rU') as req_file:
        return req_file.readlines()


setup_args = dict(
    install_requires=read_requirements_from_file(
        os.path.join(
            THIS_DIR,
            'requirements.txt')),
    tests_require=read_requirements_from_file(
        os.path.join(
            THIS_DIR,
            'requirements-dev.txt')))

setup(
    name="addie",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Need a description",
    author="Dan, Wenduo, Jean",
    author_email="oldsdp@ornl.gov, zhou@ornl.gov, bilheuxjm@ornl.gov",
    url="http://github.com/neutrons/addie",
    long_description="""Should have a longer description""",
    license="The MIT License (MIT)",
    entry_points={
        'console_scripts': [
            "addie = addie.main:main"
        ]
    },
    packages=find_packages(),
    package_data={'': ['*.ui', '*.png', '*.qrc', '*.json']},
    include_package_data=True,
    setup_requires=[],
    install_requires=setup_args["install_requires"],
    tests_require=setup_args["install_requires"] + setup_args["tests_require"],
    test_suite='tests'
)
