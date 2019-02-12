from setuptools import setup, find_packages
import os
import sys
import versioneer  # https://github.com/warner/python-versioneer

if sys.argv[-1] == 'pyuic':
    indir = 'designer'
    outdir = 'addie'
    files = os.listdir(indir)
    files = [os.path.join('designer', item) for item in files]
    files = [item for item in files if item.endswith('.ui')]

    for inname in files:
        outname = inname.replace('.ui', '.py')
        outname = outname.replace(indir, outdir)
        if os.path.exists(outname):
            print('removing {}'.format(outname))
            os.remove(outname)
    print("Did not convert any '.ui' files")
    sys.exit(0)

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
      include_package_data = True,
      #package_data={'designer': ['*.ui'],
      #              'icons':['*.png','*.qrc']},
      packages=find_packages(),
      package_dir={},
      install_requires=['numpy', 'matplotlib'],
      setup_requires=[],
      )
