# This is the shell program
# In essence this program will read the run string which will have in it:
#  Program name , Curnode and a runfile
#
# Read runfile, set up index  loop, fill invals based on runfile = value
# or get value from VF. Run code ( some in some out depth loop ) Output curves
# or ZP/GP
import adnod
import pdh_files
import os
username = "Robert Farnan"   # This needs to be case insenstive
usernode = pdh_files.unm2uns(username)
sppath = pdh_files.prnm2spath(prgnm)
print(sppath)
userpath = adnod.uns2path(usernode)
urfdepths = ['']
# From user name get user number and from user num get last user globs
fegnames = ['CURNODE', 'MODE', 'Zone', 'RFIN', 'RFOUT', 'NODECRIT']
# This is read and written to User
fegvalues= [' ',' ',' ',' ',' ',' ']
# Read User Global File an SF in Usernode for now just gets
pdh_files.rduglobf(usernode, "globals", fegnames, fegvalues)
# assign values from global file
curnode = fegvalues[0]
zone = fegvalues[2]
rfconout = fegvalues[4]
rfnamin = rfconout
path = adnod.ns2path(curnode)
print(prgnm + rfnamin + curnode)
prgnm = 'enter program name' # Enter Program Name
path = adnod.ns2path(curnode)
#  Open the runfile in Curnode
rflab = prgnm + "_" + rfnamin
rfn = pdh_files.fnm2num(curnode, 'SF', rflab)
rfpath = path + r'/s.' + rfn
rfhead = []
rfuivals = []
rfivals = []
rfovals = []
rfuovals = []
rfdepth = []
stuff = pdh_files.rdrf(rfpath, rfhead, rfuivals, rfivals, rfuovals, rfovals, rfdepth )
nin = int(rfhead[0])    # Number of inputs
nout = int(rfhead[1])  # Number of Out Curves to create by input processor
sindex = int(rfdepth[0])
npts = int(rfdepth[1])   # number of pts fron runfile rfdepth
mxpts = int(rfdepth[2])  # Mxpts in node
#  Read Each Input and determine if vector or constant
ivals = rfivals*1
ovals = rfovals*1
inhan = []
ohan = []
than = []
input('Press <ENTER> to continue')
# Open Input and Output Curves
i = 0
for v in rfuivals:
    if v[0] == 'v':
        vpath = path + r"/v." + rfivals[i]  # Picked up IC number
        han = open(vpath, 'r')
        inhan.append(han)
    else:
        inhan.append("")
    i = i+1
# now output values
i = 0
for v in rfuovals:
    if v[0] == 'v':
        vpath = path + r"/v." + rfovals[i]
        han = open(vpath, 'r')
        ohan.append(han)
        han = open(vpath + r"_tmp", 'w')
        than.append(han)
    else:
        ohan.append("")
        than.append("")
    i = i+1

# all handles and files should open and ready now thru the depth loop
ic = 1
#  first loop until start index and after end index
while ic <= mxpts:
    if ic < sindex or ic > sindex+npts-1:
        h = 0
        for v in inhan:
            if v == "":
                pass
            else:
                v.readline()
            h = h+1
        h = 0
        for v in ohan:
            if v == "":
                pass
            else:
                line = v.readline()
                than[h].write(line)
            h = h+1
#  In indexes that need calculation
    else:
        h = 0
        for v in inhan:
            if v == "":
                pass
            else:
                ivals[h] = v.readline()
                ivals[h] = ivals[h].strip('\n')
            h = h+1
#  Now insert User calculation -
#  ilabs=["a","Phi","Rw","M","N","Rt"]
        print(ic)
        a = float(ivals[0])
        phi = float(ivals[1])
        rw = float(ivals[2])
        m = float(ivals[3])
        n = float(ivals[4])
        rt = float(ivals[5])
        if a > 0 and phi >0 and rw > 0 and m > 0 and n>0 and rt > 0:
            sw = ((a/phi**m)*rw/rt)**(1/n)
        else:
            sw = -999.99

        h = 0
        for v in ohan:
            if v == "":
                pass
            else:
                v.readline()
                than[h].write(str(sw) + "\n")
            h = h+1
    ic = ic+1
# Need to read/write files to EOF should be done
# Need to close all file here plus rename tmp files
i = 0
for w in inhan:
    if rfuivals[i][0] == "v":
        w.close()
    i = i+1
i = 0
for w in ohan:
    if rfuovals[i][0] == "v":
        w.close()
        than[i].close()
        vpath = path + r"\v." + rfovals[i]
        vtmp = vpath+r"_tmp"
        os.remove(vpath)
        os.rename(vtmp, vpath)
    i = i+1
#  Loop thur handles to close ins outs and temps

# if you have zone ouput then that wil be handled here
# also need to handle case where constant is spec'd for output -
