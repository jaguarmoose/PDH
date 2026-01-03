# This is the shell program
# In essence this program will read the run string which will have in it:
#  Program name , Curnode and a runfile
#
# Read runfile, set up index  loop, fill invals based on runfile = value
# or get value from VF. Run code ( some in some out depth loop ) Output curves
# or ZP/GP
from pdh import adnod
from pdh import pdh_files
import os
import matplotlib.pyplot as plt
# current test data node (curnode) should be passed from IP
curnode = "1:1:4:18"
# curnode = input("Enter Curnode")
prgnm = 'WLPlot'
rfnamin = "RAFOUT"
# rfnamin = input("Enter RF name")
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
xvalues = []  # initialize histlist
yvalues = []
x2values = []
y2values = []
gpts = 0
sumgpts = 0
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
                if h== 0:
                    #if ivals[h] != '-999.25' and ivals[h] !='-999.99':
                    xvalues.append(ivals[h])
                    
                elif h== 1:
                    #if ivals[h] != '-999.25' and ivals[h] !='-999.99':
                    yvalues.append(ivals[h])
                    y2values.append(ivals[h])
                elif h == 2:
                    x2values.append(ivals[h])
                        #gpts = gpts + 1
                        #sumgpts = sumgpts + float(ivals[h])
                    
                        
            h = h+1
#  Now insert User calculation -
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
lx=0
rx=.5
gpts=0
g2pts = 0
xnums = []
x2nums = []
ynums = []
y2nums = []

for i,j,k in zip(xvalues, yvalues,x2values):
#    if i != '-999.25' and i !='-999.99' and j != '-999.25' and j != '-999.99': 
    xnums.append(float(i))
    y2nums.append(float(j))
    ynums.append(float(j))
    x2nums.append(float(k))
#        gpts=gpts+1
#for i,j in zip(x2values, y2values):
#    if i != '-999.25' and i !='-999.99' and j != '-999.25' and j != '-999.99': 
#        x2nums.append(float(i))
#        y2nums.append(float(j))
#        g2pts=g2pts+1
print( len(xnums), len(x2nums),len(ynums),len(y2nums))
sgpts= str(gpts)
wname= 'well_name_1:1:4:18'
plt.plot(xnums,ynums)
plt.plot(x2nums,y2nums,color = 'r')
plt.ylim(4700,4600)
plt.xlim(0,.2)
plt.fill_betweenx(ynums,xnums,x2nums,where= xnums < .1,color='g')
#plt.fill_betweenx(ynums,xnums,x2nums,where =( x2nums < xnums),color='y')
plt.title("For Well " + wname + " Number Good Pts " + sgpts )
plt.xlabel( rfuivals[0][1:])
plt.ylabel( rfuivals[1][1:])
#plt.legend()
plt.show()

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
