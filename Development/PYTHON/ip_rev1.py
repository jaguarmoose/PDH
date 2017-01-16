import sys, getopt , adnod
import pdh_files
# User is # 4 2:4 - s.0 has pointer to s.1 which is user runfile
# Data Node is 1:2 it has s.0 v.1 is poroisty v.2 rt v.3 sw s.7is archie run file
#
#
# 2. based on $RFCON it reads the runfile in from the user
# goto User Node , Find and Read last runfile for program
# Depending MODe
# 3a MODE is Interactive or Friendly,build
#    Displays input/options/output and allows user to select desired values ( friendly only parms not-defined)
#    for most fields for input user can select a constant,node gp,zone gp or a curve
# 3b Mode is run then thyis step is bypassed
#  4. Collect Depth info similar to other input values - either Zone-Node or top/base pair
# 5. IP creates new runfile
# 6. IP also any new curves are created.
# From FREND ( CURNODE,USERN,PNAME,RFCONIN,RFCONOUT,ZONE,MODE,DTYPE)
# From Frend - Data User and System Root Paths
		# Depth/Zone info is passed to program via runfile - Shell for instance

                                #open frend file for W
                                  # read globals from frend files
                                  # globals are GL.Name Value
                                  # Read until EOF find all GL.Name if name matches Global Name assign value
                                  # Global $CURMENU,$CURNODE,$HELPLEV,$LASTMLEV,$MODE,$NOABORT,$NODECRIT,$NOPROMPT,$RFCON,$TERMID
                                  #,$ZONE,$NODECRIT,$RFCON
                                  # Get user input - This will be done via a GUI twinker
                           #IMPORTANT at some time neeed to handle IP MODE
                           # alos need to do ZONE
                           # Also may need to think about a non-zone container
                           #though node GP may handle


pathd="C:/PDH/DATA"        # adnod needs work
# 0 - Set up Front End Globals
# From user name get user number and from user num get last user globs
fegnames=['CURNODE','MODE','Zone','RFIN','RFOUT','NODECRIT']
# This is read and written to User
fegvalues=['1:1:4:5','i','ZoneA','RAF_Test','RAFOUT','F']
i=0
    for a,b in zip(fegnames,fegvalues): # User Sets Globals
        print("Global "+str(i)+" " + a +" = "+b)
        i=i+1
        # This is where GUI needs

glob=''
while glob !='q':
    glob = input("Enter # of global to change , q to quite prog")
    
curnode= input("Enter curnode String")  # from FREND
nodestuff=[]
nodestuff= pdh_files.rdinf(curnode)
#,nodename,nindex,nstart,nnpts,ndi,nunits):
nname=nodestuff[0]
nameindex=nodestuff[1]
sdepth=nodestuff[2]
nindexes=nodestuff[3]
indexunits=nodestuff[4]
di=nodestuff[5]
# Setting up input for user


# read S.0 Curnode
#sdepth="1000"                 # read sdepth Curnode start depth which is Index 1
# DI='.5'
#nindexes="1000"               # read  NINDS from Curnode
curpath=adnod.ns2path(curnode)

rfconin= "RAFtest"             # RFCON from FREND actually in and out
rfpathin=curpath + r"/s.7"    # CURPATH + SF=NM2SFN(Curnode,PNAME,RFCON
zone="ZoneA"             # this is execution zone
Mode="I"                     # from FREND

#pname = Ns2Prog             #
prgnm="Archie"
pathu="C:/PDH/USER"        # read the rfcon then search the user inf file for input rcfon

usernum="4"                 # User Number from frend four how many do you want

#stuff= adnod.un2path(uns,urpath)
usfn="sf.1"                 # given user number open user s.0 , find urf =(upath, pname+rfconin)

# 1 OPEN AND READ SPEC FILE - Need PName to find SPECFile
#    Spec File contains - NIN NOUT for each input/output Label,Units,Default,Range
#    spec file is found in sys node for program program are at 3:1 each program
# Spec file is s.1 file not sure how to name py code under here
# also Help file is s.2 file
# NEED TO BUILD PROGRAM TO MAKE SPEC FILE, eventually build a shell program
paths="C:/PDH/System"      # adnod should do this
pnode = "3:1:1"             #executable program file is under system node 3:1 spec file is s.1 (orlabeled SPEC)
sppath=paths + r"/L1K1/L2K1/s.1" # This really should be found by program name
sphead=[]
sptypr=[]
splabs=[]
spdef=[]
spunits=[]
sphelp=[]
sprng=[]
stuff=pdh_files.rdspecf(sppath,sphead,sptypr,splabs,spdef,spunits,sphelp,sprng)
# SPEC file returned basic inputs that IP will ask user to input
nin=sphead[0]
nout=sphead[1]

# 2 GET Previous Inputs If Mode=U OPEN AND READ USER RUNFILE_IN If Mode=I read Data RF
# Overlay defaults from Spec with UserVals
urfpath=pathu + r"/L1K4/s.1"  # This is User 4 s.1 but should be Frend: User Num RFCON_IN
urfuvals=[]
urfdepths=[]
stuff=pdh_files.rdusrrf(urfpath,urfuvals) # This picks up last vals from user RF
                                          # If interactive Need to walk thru these on curnode and resolve
rfhead=[]
rfuivals=[]
rfivals=[]
rfuovals=[]
rfovals=[]
rfdepth=[]
if rfpathin != '':
    stuff =pdh_files.rdrf(rfpathin, rfhead, rfuivals,rfivals,rfuovals, rfovals, rfdepth)
    rfuvals=list(rfuivals+rfuovals)
    rfvals=list(rfivals+rfovals)
else:
    rfuvals=list(urfuvals)
    rfvals=list(urfuvals)
# 3 Present User with Option to select Inputs
w2c=''
while w2c!='q':
    i=0
    for a,b,c,d,e,f in zip(sptypr,splabs,rfuvals,spunits,sphelp,rfvals): # Main part of IP
        print(str(i)+" " + e +" an "+ a +" variable named "+b+ " has a value of "+ c +" "+f+" "+d)
        i=i+1
        # This is where GUI needs
    w2c = input("Enter # of variable to change , q continue")
    if w2c != 'q':
        i2c=int(w2c)
        newval= input("Enter value or vname for curve, gname GP zname for Zone")     #Need GUI
        wnewval=newval
        if newval[0]== 'v':      # will need to create new curve on exit
            wnewval=newval[1:]  # assumed user input curvename needs conversion to curve #
            wnewval = pdh_files.vnm2num(curnode,newval[1:])# vnum is # curve number #'' means not found
            if wnewval ==' ':
                print ("Robert VF file was not found - could be good or bad ")
                                         # this gets written to runfile val list
        if newval[0] == 'g':
            wnewval = pdh_files.rdgp(curnode,newval[1:])
            if wnewval == ' ':
                print("Robert you need to do something GP not found")#Need to inform user of prence
        if newval[0] == 'z':
            wnewval= pdh_files.rdzp(curnode,zone,newval[1:])
            if wnewval == ' ':
                print("Robert you need to do something ZP not found")
            
        rfuvals[i2c]=newval
        rfvals[i2c]= wnewval                              # User input is translated
for a,b,c in zip(splabs,rfuvals,rfvals):                        # from names to numbers
    print (a,b,c)


# 4 Here need iteration to Enter Depth Info
#    N- whole node Z- Zone otherwise enter a Top/Base
print ("Top Base "+sdepth)
dtype=input('Enter Depth Type , N-Node Z-Zone '' or blank - enter top/base')
if dtype == 'N' or dtype =='n':
    sindex="1"
    npts=nindexes
elif dtype=="Z" or dtype =='z':
    # need to get top base from Zone 
    fdend=float(sdepth)+float(nindexes)*float(di)-float(di)
    dend=str(fdend)
    sdep,edep=pdh_files.rdzone (curnode,zone)
    if float(sdep)<float(sdepth)or float(sdep)>fdend:
        sdep=sdepth           
    fedep=float(edep)           
    if fedep<float(sdepth)or fedep>fdend or fedep<float(sdep) :
        edep=dend           
    sindex=str(int((float(sdep)-float(sdepth))/float(di)+1))
    npts=str(int((float(edep)-float(sdep))/float(di)+1))      
    print("start depth:index "+sdep+":"+sindex+" end dep:npts "+edep+" "+npts)
    dum=input('Hit return to continue')
else:              # If Dtype=Z then zone Process- get Zone depths
    dend=str(float(sdepth)+float(nindexes)*float(di)-float(di))
    fdend=float(sdepth)+float(nindexes)*float(di)-float(di)
    dend=str(fdend)
    sdep=input('Data Start '+sdepth+' Enter start depth ')
    if float(sdep)<float(sdepth)or float(sdep)>fdend:
        sdep=sdepth           
    edep=input('Data End '+dend+' Enter end depth ')
    fedep=float(edep)           
    if fedep<float(sdepth)or fedep>fdend or fedep<float(sdep) :
        edep=dend           
    sindex=str(int((float(sdep)-float(sdepth))/float(di)+1))
    npts=str(int((float(edep)-float(sdep))/float(di)+1))      
    print("start depth:index "+sdep+":"+sindex+" end dep:npts "+edep+" "+npts)
    dum=input('Hit return to continue')
# 5 User has made all input
# Create any needed output curves
for x in (int(nin),int(nin)+int(nout)-1):
    if rfuvals[x][0]=='v' and rfvals[x]==' ': #create curve
        rfvals[x]=pdh_files.crvf(curnode,rfuvals[x][1:],"na",nindexes) # need to set units

# Now update User Runfile (IN or OUT) with new vals depth info not needed
# This depends on mode for now just rewriting
stuff = pdh_files.wrurf(urfpath,prgnm,nin,nout,rfuvals)
#Create RF/UPdate RF in Curnode
#Need to get DI data from curnode - also make sure float are handled correctly
mxpts=nindexes       # from Curnode do I need this or should Shell know
rfpathout=rfpathin    #this needs to be determined from RFCON
stuff =pdh_files.wrrf(rfpathout,prgnm,nin,nout,rfuvals,rfvals,sindex,npts,mxpts)
# At this point IP is done FREND should be able to execute prog with data node RFCON
