import sys, getopt , adnod

                                # for test purposes Spec File for Archie is s.1 in 3:1:3
                                # User is # 4 2:4 - s.0 has pointer to s.1 which is user runfile
                                # Data Node is 1:2 it has s.0 v.1 is poroisty v.2 rt v.3 sw s.1 is archie run file
			        # input processor is passed current User Number,Progname and frend file
				# contains  :program node, curnode, mode,user,
                                # 1. it also reads spec file for the program
				# Spec File - NIN NOUT for each input/output Label,Units,Default,Range	
                                # Read spec file from sys node for program program are at 3:1 each program 
                                # has a node not sure about IP and FREND - past that Archie is 3:1:3 for now
                                # Spec file is s.1 file not sure how to name py code under here 
                                # from read of spec file start to build menu to show user
                                # also Help file is s.2 file
                                # NEED TO BUILD PROGRAM TO MAKE SPEC FILE, eventually build a shell program 
                                # 2. based on $RFCON it reads the runfile in from the user
                                # goto User Node , Find and Read last runfile for program  
                                # 3. displays input/options/output and allows user to select desired values
                                # for most fields for input user can select a constant,node gp,zone gp or a curve
                                # 4. Collect Depth info
				# 5. IP creates new runfile
				# 6. IP also any new curves are created.
				# Depth/Zone info is passed to program via runfile - Shell for instance

import pdh_files
import sys
curnode= "1:2"              # frend provides curnode
di=1                        # IP picks up from Curnode DI
sdepth=1000                 # IP pick up from Curnode start depth which is Index 1
nindexes=1000               # IP picks up NINDS from Curnode
fns="2:1"                   # based on $RFCON find Runf file in user node   
pnode = "3:1:1"             # executable program file is under system node 1 spec file is s.1 no sure where exe is yet

pathu="C:/PDH/USER"        # read the rfcon then search the user inf file for input rcfon
paths="C:/PDH/System"
usernum="4"                 # User Number four how many do you want 
usfn="sf.1"                 # given user number need subroutine to open user s.0
#pname = Ns2Prog             # 
  
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
                           # 1 OPEN AND READ SPEC FILE       
                                  
sppath=paths + r"/L1K1/L2K1/s.1" # This really should be found by program name
sphead=[]
sptypr=[]
splabs=[]
spdef=[]
spunits=[]
sphelp=[]
sprng=[]
stuff=pdh_files.rdspecf(sppath,sphead,sptypr,splabs,spdef,spunits,sphelp,sprng)
# 2 OPEN AND READ USER RUNFILE FOR PROGRAM
urfpath=pathu + r"/L1K4/s.1"  # This is User 4 s.1 but should be Frend: User Num RFCON 
urfvals=[]
urfdepths=[]
stuff=pdh_files.rdusrrf(urfpath,urfvals,urfdepths) # This picks up vals from user RF
rfvals=[]
for a,b,c,d,e,f in zip(sptypr,splabs,urfvals,spunits,sphelp,sprng): # Main part of IP
    print (a,b,c,d,e,f)                                             # This is where GUI needs
    newval= input("Enter value or # for curve $GP ! for Zone")
    if newval[0]== '#':
        vnum = pdh_files.vnm2num(curnode,newval[1:])# vnum is # curve number #'' means not found
                                         # this gets written to runfile val list
    if newval[0] == '$':
         gpval = pdh_files.gp2val(curnode,newval[1:])
    if newval[0] == 'z':                        
         zval = pdh_files.zp2val(curnode,zone,newval[1:])
    rfvals.append(newval)                                           # User input is translated
for a,b in zip(splabs,rfvals):                                      # from names to numbers 
    print (a,b)
    
# Here need iteration to Enter Depth Info
dtype=input('Enter Depth Type , N-Node Z-Zone '' or blank - enter top/base')
if dtype != 'N' or dtype != 'Z':           # Note Depth is converted to Index - Need DI
    sdep=input('Enter start depth')        # In URF Depth is inft/m    
    edep=input('Enter end depth')          # IN RF converted to index


# Now update User Runfile (IN or OUT) with new vals and  
stuff= wrurf(rfpath,prgnm,nin,nout,rfvals,start,end)

#Create RF/UPdate RF in Curnode 
                                 
stuff = wrrf(rfpath,prgnm,nin,nout,rfvals,sindex,npts,mxpts)
                        
                        
