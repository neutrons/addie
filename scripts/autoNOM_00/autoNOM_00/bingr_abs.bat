@idlstart
restore,'aqdep77518.dat'
restore,'mask77518.dat'
qbinning,h9999,9999,9999,calfile='nomad_77518.calfile',sil=1,normfactor=nf9999
restore,'afsample.dat'
grouping,h9999,a9999,b9999,p9999,t9999,nf9999,mask=mask,lamfil=1,non=1,$
abskorr=1,af=af,aqdep=aqdep77518
qbinning,hback,9999,backnr,calfile='nomad_77518.calfile',sil=1,normfactor=nfback
there,nthere,dthere,eightpacks
detpos,tt
ttthere=fltarr(nthere*1024)
for i=0l,nthere-1 do begin&for j=0,7 do  ttthere((i*8+j)*128l:(i*8+j+1)*128l-1)=tt(eightpacks(i)*8+j,*)&endfor
m=min(ttthere,wm)
for i=0l,n_elements(af(0,*))-1 do af(*,i)=af(*,wm)
grouping,hback,aback,bback,pback,tback,nfback,mask=mask,lamfil=1,non=1,$
abskorr=1,af=af,aqdep=aqdep77518
makeback,aback,bback,sqrt(aback*nfback),sqrt(bback*nfback),file='backsample.dat
readmsdat,sstruc,file='sample.msdat
muscat,a9999-aback,ams9999,sstruc.muscat,normfile='norm77520.dat'
ams9999=ams9999+aback
save,a9999,b9999,t9999,p9999,nf9999,ams9999,file='all9999_c.dat'
creategr,ams9999,b9999,back='backsample.dat',norm='norm77520.dat',$
hydro=0,qminpla=10,qmaxpla=50,qmaxft=!pi*10,sc=9999,inter=0,use=0,maxr=50,$
comment='neutron, Qmax=31.414, Qdamp=0.017659, Qbroad= 0.0191822'$
,ignq=25,density=sstruc.rho,sigma=sstruc.sigmas/sstruc.packfrac,$
sbs=sstruc.sbs,sb2=sstruc.sb2,packfrac=sstruc.packfrac,d1=sstruc.radius*2,qual='_c_'
exit
