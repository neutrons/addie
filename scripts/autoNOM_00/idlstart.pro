!path=!path+':~zjn/idl'
q=findgen(2500)*.02
device,retain=2
.run fteqs
.run fteqs
.run vanratio
.run vanratio
; for experiments during and after 2016A (nexus read)
.run there15A
.run dbinningnexus
.run qbinningnexus
.run detpos16b
.run detpossola16B
.run detpossola16B
restore,'/SNS/NOM/shared/NOMpy/thetaphi14B.dat'
