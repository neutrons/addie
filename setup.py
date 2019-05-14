from setuptools import setup, find_packages
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
      entry_points = {
        'console_scripts': [
            "addie = addie.main:main"
        ]
      },
      packages=find_packages(),
      package_data={'': ['*.ui', '*.png', '*.qrc', '*.json']},
      include_package_data=True,
      install_requires=[
        'periodictable',
        'psutil',
        'QtPy' ],
      setup_requires=[],
      test_suite='tests',
      tests_require=['pytest']
      )
