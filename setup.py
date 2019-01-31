from setuptools import setup, find_packages
import os
import sys
import versioneer  # https://github.com/warner/python-versioneer

banned_ui_files=[
    'designer/ui_mainWindow.ui',
    'designer/ui_helpGui.ui',
#    'designer/step2.ui',
#    'designer/ui_launchMantid.ui',
#    'designer/ui_advanced_window.ui',
#    'designer/ui_mainWindow_no_scroll_bars.ui',
#    'designer/ui_editSq.ui',
#    'designer/step1.ui',
#    'designer/gui_fgr3.ui',
#    'designer/ui_colorStyleSetup.ui',
#    'designer/ui_jobStatus.ui',
#    'designer/ui_previewMantid.ui',
#    'designer/ui_preview_ascii.ui',
#    'designer/ui_iptsFileTransfer.ui',
#    'designer/ui_loadTableIntermediateStep.ui'
]

if sys.argv[-1] == 'pyuic':
    indir = 'designer'
    outdir = 'addie'
    files = os.listdir(indir)
    files = [os.path.join('designer', item) for item in files]
    files = [item for item in files if item.endswith('.ui')]

    done = 0
    for inname in files:
        if inname in banned_ui_files:
            print('skipping {}'.format(inname))
            continue
        outname = inname.replace('.ui', '.py')
        outname = outname.replace(indir, outdir)
        if os.path.exists(outname):
            if os.stat(inname).st_mtime < os.stat(outname).st_mtime:
                continue
        print("Converting '%s' to '%s'" % (inname, outname))
        command = "pyuic4 %s -o %s" % (inname, outname)
        os.system(command)
        done += 1
    if not done:
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
