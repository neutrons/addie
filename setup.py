from setuptools import setup, find_packages
import os
import sys
import versioneer  # https://github.com/warner/python-versioneer

setup(name="addie",
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description="Need a description",
      author="Dan, Wenduo, Jean",
      author_email="oldsdp@ornl.gov, zhou@ornl.gov, bilheuxjm@ornl.gov",
      url="http://github.com/neutrons/addie",
      long_description="""Should have a longer description""",
      license="The MIT License (MIT)",
      scripts=["scripts/addie"],
      packages=find_packages(),
      package_data={'': ['*.ui', '*.png', '*.qrc', '*.json']},
      include_package_data=True,
      install_requires=[
        'matplotlib <= 2.2.3',
        'numpy == 1.15.4',
        'periodictable == 1.5.0',
        'psutil==5.4.2',
        'QtPy==1.6.0' ],
      setup_requires=[],
)
