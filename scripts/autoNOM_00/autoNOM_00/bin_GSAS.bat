@idlstart
restore,'mask78208.dat
restore,'aqdep78208.dat'
dbinning,h9999,9999,9999,dspace,usecal=1,$
calfile='nomad_78208.calfile',sil=1,normfactor=nf9999,hz30=0
grouping,h9999,a9999,b9999,p9999,t9999,mask=mask,/non,$
aqdep=aqdep78208,q=dspace,/isgsas,lamfil=1,hz30=0,difa=difa
subdir='./'
if file_test('all_files',/dir) then subdir='all_files/
save,dspace,p9999,a9999,b9999,p9999,t9999,nf9999,filen=subdir+'all9999g.dat'
makeGSAStof,dspace,b9999,9999,9999,sqrt(b9999*nf9999),$
file='NOM9999tof.getN',/force,/tofnorm,hz30=0
makeGSAStof,dspace,b9999,9999,9999,sqrt(b9999*nf9999),$
file='NOM9999tof.gsa',back='back78210_g.dat',norm='norm78211_g.dat',$
/force,/tofnorm,hz30=0
exit
