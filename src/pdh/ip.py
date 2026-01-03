'''Input Processor Module'''

from pdh import adnod
from pdh import pdh_files
import os

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
# open frend file for W
# read globals from frend files
# globals are GL.Name Value
# Read until EOF find all GL.Name if name matches Global Name assign value
# Global $CURMENU,$CURNODE,$HELPLEV,$LASTMLEV,$MODE,$NOABORT,$NODECRIT,$NOPROMPT,$RFCON,$TERMID
#,$ZONE,$NODECRIT,$RFCON
# Also may need to think about a non-zone container
# though node GP may handle
# Steps to determine User Info
#     Based on User Name User Tree is searched for User num and User Node String is constructed
username = "Robert Farnan"   # This needs to be case insenstive
usernode = pdh_files.unm2uns(username)
sppath = ' '
while sppath == ' ':
    prgnm = input('Enter Program Name')
    sppath = pdh_files.prnm2spath(prgnm)
print(sppath)
path_pdh = os.path.abspath(__file__ + u'../../') 
path_data = os.path.join(path_pdh,'DATA') # adnod needs work
path_user = os.path.join(path_pdh,'USER')        # All this sets up User paths needs subroutine
userpath = adnod.uns2path(usernode)
urfdepths = ['']

# 0 - Set up Front End Globals
#
# From user name get user number and from user num get last user globs
fegnames = ['CURNODE', 'MODE', 'Zone', 'RFIN', 'RFOUT', 'NODECRIT']
# This is read and written to User
fegvalues = ['1:1:4:5', 'U', 'ZoneA', 'RAFOUT', 'RAFOUT', 'F']
# Read User Global File an SF in Usernode for now just gets
pdh_files.rduglobf(usernode, "globals", fegnames, fegvalues)
glob = ''
while glob != 'q':
    i = 0
    for a, b in zip(fegnames, fegvalues):  # User Sets Globals
        print("Global "+str(i)+" " + a + " = "+b)
        i = i+1
    glob = input("Enter # of global to change , c to continue,q to quite prog")
    if glob != 'q' and glob != 'c':
        gn = int(glob)
        fegvalues[gn] = input("enter new value for " + fegnames[gn])
pdh_files.wruglobf(usernode, "globals", fegnames, fegvalues)
mode = fegvalues[1]
zone = fegvalues[2]
rfconin = fegvalues[3]
rfconout = fegvalues[4]
if rfconout == '' or rfconout == ' ':
    rfconout = rfconin
# Get Curnode from global or nodecrit where nodecrit is a user nodes file name
morenodes = 1
inode = 0
nodecrit = fegvalues[5]
nodes = []
nodenames = []
if nodecrit != ' ' or nodecrit != 'f' or nodecrit != 'F':
    pdh_files.rdnodesf(usernode, nodecrit, nodes, nodenames)
while morenodes > 0:
    if nodecrit == '' or nodecrit == 'f' or nodecrit == 'F':
        curnode = fegvalues[0]
        morenodes = 0
    elif inode + 1 < len(nodes):
        curnode = nodes[inode]
        inode = inode + 1
    else:
        curnode = nodes[inode]
        morenodes = 0
        # Open Current node info file and return a list of nodestuff
    nodestuff = pdh_files.rdinf(curnode)
    #,nodename,nindex,nstart,nnpts,ndi,nunits)
    nname = nodestuff[0]
    nameindex = nodestuff[1]
    sdepth = nodestuff[2]
    nindexes = nodestuff[3]
    indexunits = nodestuff[4]
    di = nodestuff[5]
    fdi = float(di)
    fsdepth = float(sdepth)
    fnindexes = float(nindexes)
    fedepth = fsdepth + (fnindexes - 1)*fdi
    edepth = str(fedepth)
    # 1 OPEN AND READ SPEC FILE - Need PName to find SPECFile
    #    Spec File contains - NIN NOUT for each input/output Label,Units,Default,Range
    #    spec file is found in sys node for program program are at 3:1 each program
    # Spec file is s.1 file not sure how to name py code under here
    # also Help file is s.2 file
    # NEED TO BUILD PROGRAM TO MAKE SPEC FILE, eventually build a shell program
    curpath = adnod.ns2path(curnode)

    sphead = []
    sptypr = []
    splabs = []
    spdef = []
    spunits = []
    sphelp = []
    sprng = []
    stuff = pdh_files.rdspecf(sppath, sphead, sptypr, splabs, spdef, spunits, sphelp, sprng)
    # SPEC file returned basic inputs that IP will ask user to input
    nin = sphead[0]
    nout = sphead[1]

    # 2 GET Previous Inputs put in value lists for user and resolved
    #  MODE           IN         OUT        IP/DEP    PROG / Deps Passed but mode saved
    #   I            Data        Data      Full       Run
    #   U            User        Data      Full       Run
    #   R            Data        None      None       Run
    #   M            Data        User      Partial    None
    #   B            User        Data      None       None
    # Setting up input for user where this goes depends a little on mode
    rfhead = []
    rfuivals = []
    rfivals = []
    rfuovals = []
    rfovals = []
    rfdepth = []
    # Objective - on mode set up User Values- rfuvals and resolved values rfvals
    # Find Run File in User or Data Node based on mode
    rfnamin = prgnm + '_' + rfconin
    if mode == 'I' or mode == 'R' or mode == 'M':
        sfn = pdh_files.fnm2num(curnode, 'SF', rfnamin)
        rfpathin = ' '
        if sfn != ' ':
            rfpathin = curpath + r"/s."+sfn
        if rfpathin != ' ':
            pdh_files.rdrf(rfpathin, rfhead,
                           rfuivals, rfivals, rfuovals, rfovals, rfdepth)
            rfuvals = list(rfuivals+rfuovals)
            rfvals = list(rfivals+rfovals)
        else:
            rfvals = [' '] * (int(nin) + int(nout))
            rfuvals = list(spdef)
    elif mode == 'U' or mode == 'B':

        urfuvals = [] * (int(nin) + int(nout))
        urfdepths = []
        sfn = pdh_files.fnm2num(usernode, 'SF', rfnamin)
        if sfn != ' ':
            urfpath = userpath + r'/s.' + sfn
            stuff = pdh_files.rdusrrf(urfpath, urfuvals, urfdepths)
            rfuvals = list(urfuvals)
            rfvals = list(urfuvals)
        else:
            rfuvals = list(spdef)
            rfvals = [' '] * (int(nin) + int(nout))
    else:
        rfuvals = list(spdef)
        rfvals = list(spdef)
    # 2b. Resolve uvals to val based on curnode - this may depend on node
    i = 0
    for a in rfuvals:
        if a[0] == 'v':
            vnum = pdh_files.fnm2num(curnode, 'VF', a[1:])
            if vnum == ' ':
                vnum = '-999.99'
            rfvals[i] = vnum
        elif a[0] == 'g':
            gpval = pdh_files.rdgp(curnode, a[1:])
            if gpval == ' ':
                gpval = '-999.99'
            rfvals[i] = gpval
        elif a[0] == 'z':
            zval = pdh_files.rdzp(curnode, zone, a[1:])
            if zval == ' ':
                zval = '-999.99'
            rfvals[i] = zval
        else:
            rfvals[i] = a
        i = i+1
    # 3 Present User with Option to select Inputs based on mode != R or B need that
    w2c = ''
    while w2c != 'q':

        i = 0
        for a, b, c, d, e, f in zip(sptypr, splabs, rfuvals, spunits, sphelp, rfvals):  # Main part of IP
            print(str(i)+" " + e + " an " + a + " variable [ "+b + "]  " + c + " = "+f+" "+d)
            i = i+1
            # This is where GUI needs
        w2c = input("Enter # of variable to change , q continue")
        if w2c != 'q':
            i2c = int(w2c)
            newval = input("Enter value or vname for curve, gname GP zname for Zone")  # Need GUI
            wnewval = newval
            if newval[0] == 'v':      # will need to create new curve on exit
                wnewval = newval[1:]  # assumed user input curvename needs conversion to curve #
                wnewval = pdh_files.fnm2num(curnode, 'VF', newval[1:])  # vnum is # curve number #'' means not found
                if wnewval == ' ':
                    print("Robert VF file was not found - could be good or bad ")
                    # this gets written to runfile val list
            if newval[0] == 'g':
                wnewval = pdh_files.rdgp(curnode, newval[1:])
                if wnewval == ' ':
                    print("Robert you need to do something GP not found")  # Need to inform user of prence
            if newval[0] == 'z':
                wnewval = pdh_files.rdzp(curnode, zone, newval[1:])
                if wnewval == ' ':
                    print("Robert you need to do something ZP not found")

            rfuvals[i2c] = newval
            rfvals[i2c] = wnewval                              # User input is translated
    for a, b, c in zip(splabs, rfuvals, rfvals):                        # from names to numbers
        print(a, b, c)

    # 4 Here need iteration to Enter Depth Info
    # Retrieve Depth Option from run file
    # Present User with Option to select Depths based on mode != R or B need that
    #    N- whole node Z- Zone otherwise enter a Top/Base
    print("Top Base "+sdepth)
    print(" Dtype= " + urfdepths[0])
    dtype = input('Enter Depth Type , N-Node Z-Zone '' or blank - enter top/base')
    sdep = ''
    edep = ''
    if dtype == 'N' or dtype == 'n':
        urfdepths[0] = dtype
        sindex = "1"
        npts = nindexes
        print('start depth/index' + sdepth + "/" + sindex)
        print('end depth =' + edepth)
        dum = input('Hit return to continue')
    elif dtype == "Z" or dtype == 'z':
        # need to get top base from Zone
        fdend = float(sdepth)+float(nindexes)*float(di)-float(di)
        dend = str(fdend)
        sdep, edep = pdh_files.rdzone(curnode, zone)
        if float(sdep) < float(sdepth)or float(sdep) > fdend:
            sdep = sdepth
        fedep = float(edep)
        if fedep < float(sdepth)or fedep > fdend or fedep < float(sdep):
            edep = dend
        sindex = str(int((float(sdep)-float(sdepth))/float(di)+1))
        npts = str(int((float(edep)-float(sdep))/float(di)+1))
        urfdepths[0] = dtype
        print(" Dtype= " + urfdepths[0])
        print("start depth:index "+sdep+":"+sindex+" end dep:npts "+edep+" "+npts)

        dum = input('Hit return to continue')
    else:              # If Dtype not Z or N then get depths
        dend = str(float(sdepth)+float(nindexes)*float(di)-float(di))
        fdend = float(sdepth)+float(nindexes)*float(di)-float(di)
        dend = str(fdend)
        sdep = input('Data Start '+sdepth+' Enter start depth ')
        if float(sdep) < float(sdepth)or float(sdep) > fdend:
            sdep = sdepth
        edep = input('Data End '+dend+' Enter end depth ')
        fedep = float(edep)
        if fedep < float(sdepth)or fedep > fdend or fedep < float(sdep):
            edep = dend
        sindex = str(int((float(sdep)-float(sdepth))/float(di)+1))
        npts = str(int((float(edep)-float(sdep))/float(di)+1))
        print(" Dtype= " + urfdepths[0])
        print("start depth:index "+sdep+":"+sindex+" end dep:npts "+edep+" "+npts)
        dum = input('Hit return to continue')
    # 5 User has made all input
    # Create any needed output curves if MODE != R,M or B
    # if MODE
    if mode == 'I' or mode == 'U':
        if int(nout) > 0:
            for x in range(int(nin), int(nin)+int(nout)-1):
                print(rfuvals[x]+" " + rfvals[x])
                if rfuvals[x][0] == 'v' and rfvals[x] == ' ':  # create curve
                    rfvals[x] = pdh_files.crvf(curnode, rfuvals[x][1:], "na", nindexes)  # need to set units

    # Now update User Runfile (IN or OUT) with new vals depth info not needed
    # This depends on mode for if M input is written back to User node need to update
    # #  MODE           IN         OUT        IP        PROG

    #   I            Data        Data      Full       Run
    #   U            User        Data      Full       Run
    #   R            Data        None      None       Run
    #   M            Data        User      Partial    None
    #   B            User        Data      None       None
    #   also the user s.0 with a record
    # First set what output file name is
    rfnamout = prgnm + '_' + rfconout
    if mode == 'M':
        sfn = pdh_files.fnm2num(usernode, 'SF', rfnamout)
        if sfn != ' ':
            urfpath = userpath + r"/s."+sfn
            stuff = pdh_files.wrurf(urfpath, prgnm, nin, nout, rfuvals, dtype)
        else:
            urfpath, n = pdh_files.nxtsf(usernode)
            pdh_files.wrrecsf(userpath, str(n), rfnamout)
            stuff = pdh_files.wrurf(urfpath, prgnm, nin, nout, rfuvals, dtype)
    # Create RF/UPdate RF in Curnode
    # Need to get DI data from curnode - also make sure float are handled correctly
    mxpts = nindexes
    # if Mode = User or Interactive or Make  then write runfile to data node
    if mode == 'U' or mode == 'I' or mode == 'B':
        sfn = pdh_files.fnm2num(curnode, 'SF', rfnamout)
        if sfn != ' ':
            rfpathout = curpath + r"/s."+sfn
            stuff = pdh_files.wrrf(rfpathout, prgnm, nin, nout, rfuvals, rfvals, sindex, npts, mxpts)
        else:
            rfpathout, nsf = pdh_files.nxtsf(curnode)
        # append new SF record to sf and write new SF file
            pdh_files.wrrecsf(curpath, str(nsf), rfnamout)
            stuff = pdh_files.wrrf(rfpathout, prgnm, nin, nout, rfuvals, rfvals, sindex, npts, mxpts)

    # At this point IP is done FREND should execute prog if correctwith data node RFCON
    if mode != 'M' and mode != 'B':
        print("I should run " + prgnm + " on node " + nname + " Run File " + rfconout)
        print(" Depth Mode = " + dtype + " start index/npts = " + sindex + "/" + npts)
    elif mode == 'M':
        print(" Just ran Make mode")
    else:
        print(" Build Mode")
