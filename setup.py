from distutils.core import setup
import os
import sys

if sys.argv[-1] == 'pyuic':
    indir = 'designer'
    outdir = 'fastgr'
    files = os.listdir(indir)
    files = [os.path.join('designer', item) for item in files]
    files = [item for item in files if item.endswith('.ui')]

    done = 0
    for inname in files:
        outname = inname.replace('.ui', '.py')
        outname = outname.replace(indir, outdir)
        if os.path.exists(outname):
            if os.stat(inname).st_mtime < os.stat(outname).st_mtime:
                continue
        print("Converting '%s' to '%s'" % (inname, outname))
        command = "pyuic4 %s -o %s"  % (inname, outname)
        os.system(command)
        done += 1
    if not done:
        print("Did not convert any '.ui' files")
    sys.exit(0)

setup(name="FastGr",
      version="0.0.1",
#      cmdclass=versioneer.get_cmdclass(),
      description = "Need a description",
      author = "Dan Olds",
      author_email = "notsure@ornl.gov",
      url = "http://github.com/neutrons/FastGR",
      long_description = """Should have a longer description""",
      license = "The MIT License (MIT)",
      scripts=["scripts/fastgr"],
      packages=["fastgr"],
      package_dir={},
#      data_files=[('/etc/bash_completion.d/', ['gui_fgr3.ui'])]
)
