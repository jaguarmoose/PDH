import pdh_files
import adnod
curnode=input("Enter Curnode")
nodestuff=[]
nodestuff= pdh_files.rdinf(curnode)
#,nodename,nindex,nstart,nnpts,ndi,nunits):
nname=nodestuff[0]
nameindex=nodestuff[1]
sdepth=nodestuff[2]
nindexes=nodestuff[3]
indexunits=nodestuff[4]
di=nodestuff[5]

vunits="Dec"
vlabel="SW_RAF"
stuff=pdh_files.crvf(curnode,vlabel,vunits,nindexes)
#vpath=adnod.ns2path(ns)+ r"\v.2"
#vdata=[".11"]*ninx  # Rt written as 50.2 Pore as .11
#stuff=pdh_files.upvf(vpath,sinx,ninx,minx,vdata)
