from pdh import pdh_files
from pdh import adnod
ns="1:2"
label="Twilight"
path=adnod.ns2path(ns)+ "\s.0"
iname="Depth"
units="Feet"
si=str(1000)
npts=str(1000)
di=str(.5)
#stuff=pdh_files.crinf(ns,label,iname,units,si,npts,di)
#stuff=pdh_files.crzf(ns,label)
#stuff=pdh_files.upsf(path)
vunits="Dec"
vlabel="Pore"
#stuff=pdh_files.crvf(ns,vlabel,vunits)
vpath=adnod.ns2path(ns)+ r"\v.2"
sinx=200
ninx=500
minx=1000
vdata=[".11"]*ninx  # Rt written as 50.2 Pore as .11 
stuff=pdh_files.upvf(vpath,sinx,ninx,minx,vdata) 

