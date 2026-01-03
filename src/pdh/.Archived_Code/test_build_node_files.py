from pdh import pdh_files
from pdh import adnod
ureq=' '
while ureq != 'q':
    ureq=input("Enter q to quit, n for new node, g for gp")
# Enter Parent Node string
    if ureq == 'n':
        pns=input(" Enter a parent node string")
        curnode=adnod.nxtkid(pns)
        print("curnode= ",curnode)
        label=input("Enter Node Name")
        iname=input("Enter Index Name")
        units=input("Enter Index Units")
        si=input("Enter Start Value for "+iname+" in "+ label)
        npts=input("Enter Number of Points")
        di=input("Enter "+ units + "Increment")
        stuff=pdh_files.crinf(curnode,label,iname,units,si,npts,di)
    elif ureq == 'g':
        curnode=input("Enter Curnode")
        curpath=adnod.ns2path(curnode)
        infpath=curpath+r"/s.0"
        nodestuff=[]
        nodestuff= pdh_files.rdinf(curnode)
        #,nodename,nindex,nstart,nnpts,ndi,nunits):
        nname=nodestuff[0]
        nameindex=nodestuff[1]
        sdepth=nodestuff[2]
        nindexes=nodestuff[3]
        indexunits=nodestuff[4]
        di=nodestuff[5]
        w2w=''
        while w2w != 'q':
            w2w=input("Z new Zone,z new ZP, g to write GP,v to write curve q-quit")
            if w2w =='G' or w2w=='g':
                gpnam=input("GP Name")
                gpvalue=input("GP Value")
                gpunits=input("GP Units")
                stuff=pdh_files.wrgp(infpath,gpnam,gpvalue,gpunits)
            elif w2w =='V'or w2w=='v':
                vlabel = input("Curve Name")
                vunits = input("Curve Units")
                nval=input("Curve default value ,if blank -999.99")
                if nval =='' or nval ==' ':
                    nval='-999.99'
                stuff=pdh_files.crvf(curnode,vlabel,vunits,nindexes,nval)
            elif w2w =='Z':
                zname=input("Enter New Zone Name")
                ztop=input("Enter New Zone Top")
                zbase=input("Enter New Zone Base")
                pdh_files.wrzone(curnode,zname,ztop,zbase)
            elif w2w =='z':
                zonenm=input("Enter Current Zone Name")
                zpname=input("Enter Zone Parm Name")
                zpvalue=input("Enter Zone Parm Value")
                zpunits=input("Enter Zone Parm Units")
                pdh_files.wrzp(curnode,zonenm,zpname,zpvalue,zpunits=' ')
#vpath=adnod.ns2path(ns)+ r"\v.2"
#vdata=[".11"]*ninx  # Rt written as 50.2 Pore as .11
#stuff=pdh_files.upvf(vpath,sinx,ninx,minx,vdata)

