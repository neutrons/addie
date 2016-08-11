@idlstart
restore,'mask77518.dat
restore,'aqdep77518.dat'
qbinning,h9999,9999,9999,calfile='nomad_77518.calfile',sil=1,normfactor=nf9999,hz30=0
grouping,h9999,a9999,b9999,p9999,t9999,mask=mask,lamfil=1,$
/non,aqdep=aqdep77518,hz30=0,difa=difa
subdir='./'
if file_test('all_files',/dir) then subdir='all_files/'
save,p9999,a9999,b9999,p9999,t9999,nf9999,filen=subdir+'all9999.dat'
creategr,a9999,b9999,back='back77519.dat',norm='norm77520.dat',$
hydro=0,qminpla=10,qmaxpla=50,qmaxft=!pi*10,sc=9999,inter=0,use=1,maxr=50,$
comment='neutron, Qmax=31.414, Qdamp=0.017659, Qbroad= 0.0191822'$
,ignq=25,error=sqrt(a9999*nf9999)
exit
