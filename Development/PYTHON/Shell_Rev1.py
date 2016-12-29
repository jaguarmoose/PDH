# This is the shell program
# In essence this program will read the run string which will have in it
# the name of a runfile which this program will interpret
# let's start with Archie
# Sw = (F * Rw/FT) ^ 1/n where F=a/Phi^M
# Frend was told to run archie , that invoked the Input Processor (IP)
# the IP looked first in the Sys Node to retrieve the SpecFile for Archie
# that said there were 6 input values and 1 output value,
# IP then read loaded default values from the sys default file.
# IN interactive Mode the IP presented this info to user and it was saved in
# USer RFCON file for that Node ( all constants were resolved) 
# the Shell PRogram picked up this file
# For Each of 6 input they were defined as was the name of output
# For Archie as example File Might look like
# NI=6 NO=1
# IN_1.A 1
# IN_2.Phi #4     -Retrieve from VF4 in this node
# IN_3.Rw .08
# IN_4.M 2
# IN_5.N 2
# In_6.RT #88
# OU_1.SW #92
# DI StartI=100 NI=4  - In this node process 4 levels starting at level 100
# Shell Program has following step
# Read runfile, set up index  loop, fill invals based on runfile = value
# or get value from VF. Run code ( some in some out depth loop ) Output curves
# or ZP/GP
#
#

#
#NI,NO = RDRF(Runfile) # RDRF returns #IN,#OUT array of assigments
import adnod, pdh_files
import os
ns="1:2"   # runfile needs to have runstring too
path=adnod.ns2path(ns)
           # open runfile - given program name and Rfcon label find file in
rfpath=path+ r'\s.1'  # the cur node s.0 rf_path=NSLAB2PATH
           # Read from runfile somewhere convert SDEPTH to INDEX done in IP? 
#DI=.5    # Read from runfile may not need DI in runfile
         #rdrf(rfpath,rfhead,rfivals,rfovals,rfdepth)
rfhead=[]
rfivals=[]
rfovals=[]
rfdepth=[]
stuff=pdh_files.rdrf(rfpath,rfhead,rfivals,rfovals,rfdepth)
nin=int(rfhead[0])# 
nout=int(rfhead[1]) # Needed Out files are created by input processor
sindex=int(rfdepth[0])
npts=int(rfdepth[1]) # Read fron runfile rfdepth
mxpts=int(rfdepth[2]) # Read from runfile
         # Read Each Input and determine if vector or constant
         # Basically read thru runfile and assign Values these values then
         # get assigned to input values
         # Need function read runfile and pass of input output values 
#ilabs=["a","Phi","Rw","M","N","Rt"] # should be filled from reading runfile
#ivals=["1","#2",".08","2","2","#1"]
ivals=rfivals*1
oivals=ivals*1
#olabs=["Sw"]
#ovals=["#3"]
ovals=rfovals*1
oovals=ovals*1
inhan=[] # Create a list to handle file handles
ohan=[]   # Read the run file and for each record if IO fill the list
than=[]          # with lists full from run file now get index
          # loop thru list to create give each file a handle
input('Press <ENTER> to continue')
# Open Input and Output files

for v in ivals:
    if v[0]=='#':
        vpath=path+r"\v."+ v[1:]
        han=open(vpath,'r')
        inhan.append(han)
    else:
        inhan.append("")
# now output values

for v in ovals:
    if v[0]=='#':
        vpath=path+r"\v."+ v[1:]
        han=open(vpath,'r')
        ohan.append(han)
        han=open(vpath+r"_tmp",'w')
        than.append(han)
    else:
        ohan.append("")
        than.append("")
      
# all handles and files should open and ready now thru the depth loop    

ic=1
                   # first loop until start index
while ic < mxpts:
    if ic < sindex or ic > sindex+npts-1 :   # and loop after end index
        h=0
        for v in inhan :
            if v =="":
                pass
            else:
                v.readline()
            h=h+1   
        h=0
        for v in ohan:
            if v =="":
                pass
            else:
                line=v.readline()
                than[h].write(line)
                
            h=h+1        
  
    else:                           # In indexes that need calculation
        h=0
        for v in inhan :
            if v =="":
                pass
            else:
                ivals[h]=v.readline()
                ivals[h]=ivals[h].strip('\n')
            h=h+1
                                #Now User calculation
#ilabs=["a","Phi","Rw","M","N","Rt"] 
#["1","#4","2","2","#88"]
        a=float(ivals[0])
        phi=float(ivals[1])
        rw=float(ivals[2])
        m=float(ivals[3])
        n=float(ivals[4])
        rt=float(ivals[5])
        sw=((a/phi**m)*rw/rt)**(1/n)
        h=0    
        for v in ohan:
            if v =="":
                pass
            else:
                v.readline()
                than[h].write(str(sw) +"\n")
            h=h+1
    ic=ic+1
# Need to read/write files to EOF should be done
# Need to close all file here plus rename tmp files
i=0
for w in inhan:
    if oivals[i][0] == "#":
        w.close()
    i=i+1    
i=0
for w in ohan:
    if oovals[i][0] == "#":
        w.close()
        than[i].close()
        vpath=path+r"\v."+ oovals[i][1:]
        vtmp = vpath+r"_tmp"
        os.remove(vpath)
        os.rename(vtmp,vpath)
    i=i+1
#Loop thur handles to close ins outs and temps

# if you have zone ouput then that wil be handled here
