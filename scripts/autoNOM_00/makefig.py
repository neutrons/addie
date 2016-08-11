from optparse import OptionParser
from subprocess import Popen
from time import sleep
import pdb
import shlex
import glob
import sys
import stat
#import matplotlib.pyplot as plt
from os import listdir,getcwd,popen
#sys.path.append("/SNS/NOM/shared/NOMpy")
pydir = '/SNS/users/zjn/pytest'
sys.path.append(pydir)
from NOMpy import *

# ************************ parse command line options ********************

parser = OptionParser()
parser.add_option("-s", "--scannr", dest="scannr",
                  help="current scan Nr")
options, args = parser.parse_args()

# ************************ interpret command line options ********************
scannr=options.scannr
if not scannr:
    anyanalized=anyftl()
    if not anyanalized:
        exit()
    scannr=lastftl()

filename='NOM_'+str(scannr)+'ftl.dat'
#pdb.set_trace()
#(r,ft)=rstd(filename)

# cant figure out how to get the labels right, let's gnuplot it

#plt.plot(r,ft)
#font = {'family' : 'serif',
#        'weight' : 'normal',
#        'size'   : 16,
#        }
#plt.xlabel('r/ A', fontdict=font)
#plt.ylabel('g(r)', fontdict=font)
#plt.set_xticks([0, 10,20])
#plt.set_xticklabels(['0', '$\pi$','2$\pi$'])
#plt.rc('font', **font)

#plt.savefig('foo.png')

for i in range(4):
    Lline='rm -f fig'+str(i)+'.gnu'
    Popen(shlex.split(Lline))
    Lline='rm -f fig'+str(i)+'.ps'
    Popen(shlex.split(Lline))
    Lline='rm -f fig'+str(i)+'.pdf'
    Popen(shlex.split(Lline))
ipts=findcurrentipts()
#outfile='/SNS/NOM/IPTS-'+str(ipts)+'/shared/autoNOM/figs/NOM_'
outfile='./figs/NOM_'
outfile+=str(scannr)+'_autoreduced_temp.png'
currentplot='/SNS/users/zjn/LiveData/currentplot.png'
oldfiles=[outfile,'temp1.png','temp2.png',currentplot,'fig1.pdf','fig2.pdf','fig3.pdf','fig4.pdf']
cleanup_files(oldfiles)





f=open('fig1.gnu','w')
lines=['set term post color 24 sol land',
"set out 'fig1.ps'",
"set enc iso",
"set title 'Scan scan'" ,
"set xla 'r / \305",
"set yla 'A [g(r)-1]",
"plot [1:10] 'NOM_scanftl.dat' tit '' w l lt 3,'NOM_scanftnat.dat' tit '' w p pt 3,'NOM_scanftf.dat' tit '' w l lt 1",
"set out",
"exit"]
for line in lines:
    line=line.replace('scan',str(scannr))
    print >>f,line
f.close()
Lline="gnuplot fig1.gnu"
Popen(shlex.split(Lline))

f=open('fig2.gnu','w')
lines=['set term post color 24 sol land',
"set out 'fig2.ps'",
"set enc iso",
"set title 'Scan scan'" ,
"set xla 'r / \305",
"set yla 'PDF = A r[g(r)-1] / \305",
"plot [0:30] 'NOM_scanftlrgr.gr' tit '' w l lt 3 lw 3,'NOM_scanftnat.dat' u ($1):($2*$1):($3*$1) tit '' w p pt 3,'NOM_scanftfrgr.gr' tit '' w l lt 1",
"set out",
"exit"]
for line in lines:
    line=line.replace('scan',str(scannr))
    print >>f,line
f.close()
Lline="gnuplot fig2.gnu"
Popen(shlex.split(Lline))

f=open('fig3.gnu','w')
lines=['set term post color 24 sol land',
"set out 'fig3.ps'",
"set enc iso",
"set title 'Scan scan'" ,
"set xla 'Q / \305^{-1}",
"set yla 'A [S(Q)-1]'",
"plot  [0.25:30] 'NOM_scanSQ.dat' tit ''w l,'NOM_scanSQ.dat' tit '' w e",
"set out",
"exit"]
for line in lines:
    line=line.replace('scan',str(scannr))
    print >>f,line
f.close()
Lline="gnuplot fig3.gnu"
Popen(shlex.split(Lline))

filename='NOMscantof-4.dat'
filename=[filename.replace('scan',str(scannr))]
exist=test_fileexist(filename,'.')
if exist:
	(tof,bank4)=rstd(filename[0])
	i=[i[0] for i in bank4] 
	maxi=max(i[500:2900])
	mini=min(i[500:2900])
	f=open('fig4.gnu','w')
	lines=['set term post color 10 sol land enh ',
	"set out 'fig4.ps'",
	"set enc iso",
	"set bmargin 2",
	"set tmargin 2",
	"set lmargin 2",
	"set rmargin 2",
	"set xla 'd / \305",
	"set yla 'Int(d)'",
	"set multiplot layout 2,3 title 'Scan scan'",
	       "plot [0:1.5]'NOMscantof-4.dat'  u($1/10590.89):($2) :($3) tit '2 theta 154 deg' w e,'NOMscantof-4.dat'  u($1/10590.89):($2) tit '' w l lt 3 lw 1 ",
	       "plot [0.2:1.8]'NOMscantof-3.dat'  u($1/9506.65):($2) :($3) tit '2 theta 122 deg'w e,'NOMscantof-3.dat'  u($1/9506.65):($2) tit '' w l lt 3 lw 1 ",
	       "plot [0.2:3.5] 'NOMscantof-2.dat' u($1/5999.26):($2) :($3) tit '2 theta 67 deg' w e,'NOMscantof-2.dat'  u($1/5999.26):($2) tit '' w l lt 3 lw 1 ",
	"plot [0.3:6.5]'NOMscantof-1.dat'  u($1/2904.74):($2) :($3) tit '2 theta 31 deg' w e,'NOMscantof-1.dat'  u($1/2904.74):($2) tit '' w l lt 3 lw 1 ",
	"plot [.5:11] 'NOMscantof-0.dat'  u($1/1418.75):($2) :($3) tit '2 theta 15 deg' w e,'NOMscantof-0.dat'  u($1/1418.75):($2) tit '' w l lt 3 lw 1 ",
	"plot [.7:25] 'NOMscantof-5.dat' u($1/663.565):($2) :($3) tit '2 theta  7 deg'  w e,'NOMscantof-5.dat'  u($1/663.565):($2) tit '' w l lt 3 lw 1 ",
	"unset multiplot",
	"set out",
	"exit"]
	for line in lines:
  		  line=line.replace('scan',str(scannr))
   		  line=line.replace('theta','/theta')
   		  line=line.replace('maxi',str(maxi))
   		  line=line.replace('mini',str(mini))
    		  print >>f,line
	f.close()
	Lline="gnuplot fig4.gnu"
	Popen(shlex.split(Lline))
	while not test_fileexist(['fig4.ps'],'.'):
            sleep(5)
while not test_fileexist(['fig1.ps','fig2.ps','fig3.ps'],'.'):
        sleep(5)

Lline="convert fig1.ps fig1.pdf"
Popen(shlex.split(Lline))
Lline="convert fig2.ps fig2.pdf"
Popen(shlex.split(Lline))
print test_fileexist(['fig3.ps'],'.')

Lline="convert fig3.ps fig3.pdf"
Popen(shlex.split(Lline))
fig4exists=test_fileexist(['fig4.ps'],'.')
while not test_fileexist(['fig3.pdf','fig2.pdf','fig1.pdf'],'.'):
    sleep(5)
if fig4exists:
    Lline="convert fig4.ps fig4.pdf"
    Popen(shlex.split(Lline))
    while not test_fileexist(['fig4.pdf'],'.'):
        sleep(5)

#pdb.set_trace()
print fig4exists

if fig4exists:
    Lline="convert fig1.pdf fig2.pdf +append temp1.png"
    Popen(shlex.split(Lline))
    Lline="convert fig3.pdf fig4.pdf +append temp2.png"
    Popen(shlex.split(Lline))
    while not test_fileexist(['temp1.png','temp2.png'],'.'):        
        sleep(5)
    glob.glob('temp*')
    Lline="convert temp1.png temp2.png -append "+outfile
    Popen(shlex.split(Lline))
    while not test_fileexist([outfile[7:]],'figs'):
        sleep(5)
    Lline="rm -f temp2.png"
    Popen(shlex.split(Lline))
elif True:
    Lline="convert fig1.pdf fig2.pdf +append temp1.png"
    Popen(shlex.split(Lline))
    while not test_fileexist(['temp1.png'],'.'):
        sleep(5)
    Lline="convert temp1.png fig3.pdf -append "+outfile
    Popen(shlex.split(Lline))
    while not test_fileexist([outfile[7:]],'figs'):
        sleep(5)

Lline="rm temp1.png"
Popen(shlex.split(Lline))

Lline="cp "+outfile+" "+currentplot
print Lline
Popen(shlex.split(Lline))
sleep(5)
"""Lline="cp "+outfile+" figs" 
Popen(shlex.split(Lline))
Lline="cp fig1.pdf figs/fig1_scan.pdf"
Lline=Lline.replace('scan',str(scannr))
Popen(shlex.split(Lline))
Lline="cp fig2.pdf figs/fig2_scan.pdf"
Lline=Lline.replace('scan',str(scannr))
Popen(shlex.split(Lline))
Lline="cp fig3.pdf figs/fig3_scan.pdf"
Lline=Lline.replace('scan',str(scannr))
Popen(shlex.split(Lline))
Lline="cp fig4.pdf figs/fig4_scan.pdf"
Lline=Lline.replace('scan',str(scannr))
Popen(shlex.split(Lline))
"""

try:
    os.chown(currentplot, -1, 43217) # sns_nom_team
except OSError:
    pass

try:
    os.chmod(currentplot, stat.S_IRWXU | stat.S_IRWXG \
         | stat.S_IROTH | stat.S_IXOTH)
except OSError:
    pass


#Lline="convert fig1.pdf /SNS/NOM/shared/plots/fig1.png"
#Popen(shlex.split(Lline))
#Lline="convert fig2.pdf /SNS/NOM/shared/plots/fig2.png"
#Popen(shlex.split(Lline))
#Lline="convert fig3.pdf /SNS/NOM/shared/plots/fig3.png"
#Popen(shlex.split(Lline))
#Lline="convert fig4.pdf /SNS/NOM/shared/plots/fig4.png"
#Popen(shlex.split(Lline))"""



