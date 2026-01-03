import ast
import os
import sys

from pdh import adnod

# Create an info file given a NodeString
# Need to error check for directory and file then return
def crinf(ns: str, label: str, iname: str, units: str, si: str, npts: str, di: str) -> None:
    """crinf."""
    path = adnod.ns2path(ns)
    path= path + "\s.0"
    fso=open(path,"w")
    rec={'Rtype':'HD','Name':label}
    s=str(rec)
    fso.write(s+ "\n")
    recdi={'Rtype':'DI','Index':iname,"Units":units,"Start":si,"Npts":npts,"DI":di}
    s=str(recdi)
    fso.write(s+ "\n")
    fso.close()
def rdinf(ns: str) -> list[str]:
    """rdinf."""
    nlist=[]
    path = adnod.ns2path(ns)
    path= path + "\s.0"
    fso=open(path,"r")
    for line in fso.readlines(): # There are 4 types of records HD ,DI
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] == 'HD':
                nlist.append(d['Name'])
            elif d['Rtype']=='DI':
                nlist.append(d['Index']) #
                nlist.append(d['Start']) #
                nlist.append(d['Npts']) #
                nlist.append(d['Units'])
                nlist.append(d['DI'])
    fso.close()
    return nlist

def crdi(path: str, label: str, npts: str, start: str, units: str) -> None:
    """crdi."""
    fo=open(path,"a")
    for line in fo.readlines():
         line=line.strip('\n')
         d={line}
                      # if rectype = DI update those values
         oline=line + "\n"
         fo.write(oline)
def rdzone(curnode: str, zname: str) -> tuple[str, str]:
    """rdzone."""
    curpath=adnod.ns2path(curnode)    # gp to value
    infpath=curpath+"/s.0"
    infhan=open(infpath,"r")
    ztop=' '
    zbase=' '
    for line in infhan.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] =='ZO' and d['Name']==zname :
                ztop=d['ZTop']
                zbase=d['ZBase']
                infhan.close()
                return ztop,zbase
    infhan.close()
    return ztop,zbase
def wrzone(curnode: str, zonenm: str, ztop: str, zbase: str) -> None:
    """wrzone."""
    dum1,dum2= rdzone(curnode,zonenm)
    if dum1 ==' ':
        curpath=adnod.ns2path(curnode)    # gp to value
        infpath=curpath+"/s.0"
        infhan=open(infpath,"a")
        zrec=str({'Rtype':'ZO','Name':zonenm,'ZTop': ztop,'ZBase':zbase})
        oline=zrec + "\n"
        infhan.write(oline)
        infhan.close()
        return
    return
def wrzp(curnode: str, zonenm: str, zpname: str, zpvalue: str, zpunits: str = ' ') -> None:
    """wrzp."""
    curpath=adnod.ns2path(curnode)    # gp to value
    path=curpath+"/s.0"
    infile=path                 # if record not found append to file
    outfile=path+"tmp"
    fi=open(infile, 'r') # open file for reading
    fo=open(outfile,'w') # open file for appending
    w='t'
    for line in fi.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] =='ZP' and d['Name']==zpname and d['Zone']== zonenm : #Need to write ZP
                w='f'
                if zpunits==' ':
                    zpunits=d['Unit']
                #{'Unit': 'yes', 'Value': '.05', 'Name': 'Rw', 'Rtype': 'ZP','Zone':zonename}
                rec1=str({'Rtype':'ZP','Name':zpname,'Value':zpvalue,'Unit':zpunits,'Zone':zonenm},)
                oline=rec1 + "\n"
                fo.write(oline)
            else:
                oline=line + "\n"
                fo.write(oline)
    if w =='t':
        rec1=str({'Rtype':'ZP','Name':zpname,'Value':zpvalue,'Unit':zpunits,'Zone':zonenm})
        oline=rec1 + "\n"
        fo.write(oline)
    fi.close()
    fo.close()
    os.remove(infile)
    os.rename(outfile,infile)
    return


def rdzp(curnode: str, zonenm: str, zpname: str) -> str:
    """rdzp."""
    curpath=adnod.ns2path(curnode)    # gp to value
    infpath=curpath+"/s.0"
    infhan=open(infpath,"r")
    zvalue=' '
    for line in infhan.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] =='ZP' and d['Name']==zpname and d['Zone'] == zonenm:
                zvalue=d['Value']
                infhan.close()
                return zvalue;
    infhan.close()
    return zvalue;
def nxtsf(ns: str) -> tuple[str, int]:
    """nxtsf."""
    n=1
    if ns[0] == '2':
        ipath=adnod.uns2path(ns)
    else:
        ipath = adnod.ns2path(ns)
    path=ipath+"\s."+str(n)
    while os.path.isfile(path):
        n=n+1
        path=ipath+"\s."+str(n)
    return path,n
def crvf(ns: str, name: str, units: str, npts: str, nval: float = -999.99) -> str:
    """crvf."""
     #Create a Vector File, updated: include npts in call nval in call default
    path = adnod.ns2path(ns) # open the inf file to read
                             # This should be read from DI record on INF
    path=path +"\s.0"
    print(path)
    finf=open(path,"r")# read inf to see if VF already exists
    for line in finf.readlines():  # problem if file has blanks before eof
         line=line.strip('\n')
         if len(line)> 1:          # this code seems to trap blank lines before
             d=ast.literal_eval(line)# EOF not sure I like it
             print (d["Rtype"])
             if  d["Rtype"] == "VF":
                 if d["Name"] == name: #VF is already present
                     finf.close()
                     return
    finf.close()
    finf=open(path,"a")
    vpath,n=nxtvf(ns)
    print ("Im Here")
    recvf={'Rtype':'VF','Name': name,'FileNum': n,'Units':units}
    s=str(recvf)
    finf.write(s+ "\n")      # wrote dict as VF record to INF
    finf.close()
    vpath,n= nxtvf(ns)    # read all VF. to see that label doesn't exist
    print(vpath,n)
    fvf=open(vpath,'w')      # if it does don't create, exit
    index=0
    npts=int(npts)
    while index < npts:
        fvf.write(str(nval)+ "\n")   # read DI record from INF get Sd,NPT,DI
        index=index+1
    fvf.close()              # write the new VF record to inf
    return n;
def nxtvf(ns: str) -> tuple[str, int]:
    """nxtvf."""
    n=1
    rpath = adnod.ns2path(ns)
    path=rpath+r"\v."+str(n)
    while os.path.isfile(path):
        n=n+1
        path=rpath+r"\v."+str(n)
    return path,str(n)

def upsf(path: str) -> None:
    """upsf."""
    infile=path                 # if record not found append to file
    outfile=path+"tmp"
    fi=open(infile, 'r') # open file for reading
    fo=open(outfile,'a') # open file for appending
    for line in fi.readlines():
         line=line.strip('\n')
         d={line}
         print (line, str(d))
         oline=line + "\n"
         fo.write(oline)
    rec1={'Rtype':'GP','Name':'Rw','Value':".05",'Unit':'Ohm-m'}
    a=str(rec1['Rtype'])
    print (a)
    s=str(rec1)
    fo.write(s+ "\n")
    fi.close()
    fo.close()
    os.remove(infile)
    os.rename(outfile,infile)
def rdgp(curnode: str, gpname: str) -> str:
    """rdgp."""
    curpath=adnod.ns2path(curnode)    # gp to value
    infpath=curpath+"/s.0"
    infhan=open(infpath,"r")
    for line in infhan.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] =='GP' and d['Name']==gpname :
                gpval=d['Value']
                infhan.close()
                return gpval
    infhan.close()
    gpval=' '
    return gpval

def wrgp(path: str, name: str, value: str, units: str) -> None:
    """wrgp."""
    infile=path                 # if record not found append to file
    outfile=path+"tmp"
    fi=open(infile, 'r') # open file for reading
    fo=open(outfile,'w') # open file for appending
    w='t'
    for line in fi.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] =='GP' and d['Name']==name : #Need to write GP
                w='f'
                units=d['Unit']
                rec1=str({'Rtype':'GP','Name':name,'Value':value,'Unit':units})
                oline=rec1 + "\n"
                fo.write(oline)
            else:
                oline=line + "\n"
                fo.write(oline)
    if w =='t':
        rec1=str({'Rtype':'GP','Name':name,'Value': value,'Unit':units})
        oline=rec1 + "\n"
        fo.write(oline)
    fi.close()
    fo.close()
    os.remove(infile)
    os.rename(outfile,infile)
    return

def wrrecvf(path: str, n: str, name: str, units: str) -> None:
    """wrrecvf."""
    finf=open(path+"s.0","a")
    recvf={'Rtype':'VF','Name': name,'FileNum': n,'Units':units}
    return
def wrrecsf(path: str, n: str, name: str, kind: str = '') -> None:
    """wrrecsf."""
    finf=open(path+"\s.0","a")
    recsf=str({'Rtype':'SF','Name': name,'FileNum': n,'Kind':kind})
    oline=recsf + "\n"
    finf.write(oline)
    finf.close()
    fsf=open(path +"s."+n,'w')
    fsf.write(str({'Rtype':'HD','Name': name})+'\n')
    fsf.close()
    return
def upvf(vpath: str, sinx: str, ninx: str, minx: str, vdata: list[str]) -> None:
    """upvf."""
    print(vpath)
    fv=open(vpath,'r')
    ftmp=open(vpath + r"_tmp",'w')
    ic=1
    vi=0               # first loop until start index
    while ic < minx:
        if ic < sinx or ic > sinx+ninx-1 :   # and loop after end index
            dum=fv.readline()
            print (dum)
            dum=dum.strip('\n')
            ftmp.write(dum+'\n')
        else:                          # In indexes that need calculation
            dum=fv.readline()
            ftmp.write(vdata[vi]+'\n')
            vi=vi+1
        ic=ic+1
    fv.close()
    ftmp.close()
    os.remove(vpath)
    os.rename(vpath +r"_tmp",vpath)


def rdrf(rfpath: str, rfhead: list[str], rfuivals: list[str], rfivals: list[str], rfuovals: list[str], rfovals: list[str], rfdepth: list[str]) -> None:
    """rdrf."""

    rfhan=open(rfpath,'r') # This is where the function to read a runfile goes
    for line in rfhan.readlines(): # There are 4 types of records HD ,IN,OUT,DEPTH
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] == 'HD':
                rfhead.append(d['NIN']) #
                rfhead.append(d['NOUT']) #
                rfhead.append(d['Prgnm'])#
            elif d['Rtype'] == 'IN':
                rfivals.append(d['val'])
                rfuivals.append(d['uval'])
            elif d['Rtype'] == 'OUT':
                rfuovals.append(d['uval'])
                rfovals.append(d['val'])

            elif d['Rtype'] == 'DEPTH':
                rfdepth.append(d['Start'])
                rfdepth.append(d['NPTS'])
                rfdepth.append(d['MXPTS'])
    rfhan.close()
    return
def rdspecf(sppath: str, sphead: list[str], sptypr: list[str], splabs: list[str], spdef: list[str], spunits: list[str], sphelp: list[str], sprng: list[str]) -> None:
    """rdspecf."""
    sphan=open(sppath,'r') # Open Program Spec file
    for line in sphan.readlines():
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] == 'HD':
                sphead.append(d['NIN']) #
                sphead.append(d['NOUT']) #
                sphead.append(d['Prgnm'])#
            else:
                sptypr.append(d['Rtype'])
                splabs.append(d['label'])
                spdef.append(d['def'])
                spunits.append(d['units'])
                sphelp.append(d['help'])
                sprng.append(d['range'])
    sphan.close()
    return
def rdusrrf(urfpath: str, urfuvals: list[str], dt: list[str]) -> None:
    """rdusrrf."""
    urfhan=open(urfpath,'r') # Open User Run File
    for line in urfhan.readlines():
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype']== 'IN' or d['Rtype']== 'OUT':
                urfuvals.append(d['uval']) #
            elif d['Rtype'] == 'DEPTH':
                dt.append(d['Type'])
            #    urfdepths.append(d['Start'])
            #    urfdepths.append(d['End'])
    urfhan.close()
    return
def wrrf(rfpath: str, prgnm: str, nin: str, nout: str, rfuvals: list[str], rfvals: list[str], sindex: str, npts: str, mxpts: str) -> None:
    """wrrf."""
    rfhan=open(rfpath,'w')
    recrfhd={'Ftype': 'Run', 'Rtype': 'HD','Prgnm':prgnm,'NIN':nin,'NOUT':nout}
    s=str(recrfhd)
    rfhan.write(s + '\n')
    i=0
    while i < int(nin)+ int(nout):
        if i < int(nin):
            recrfvl={'Rtype': 'IN','uval':rfuvals[i],'val':rfvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        else:
            recrfvl={'Rtype': 'OUT','uval':rfuvals[i],'val':rfvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        i=i+1
    recrfdep= {'Rtype': 'DEPTH','Start': sindex,'NPTS': npts,'MXPTS': mxpts}
    s=str(recrfdep)
    rfhan.write(s + '\n')
    rfhan.close()
    return
def wrurf(rfpath: str, prgnm: str, nin: str, nout: str, rfuvals: list[str], dt: list[str]) -> None:
    """wrurf."""
    # biggest way this differs from runfile is depth is in DI units and curves GPs are named
    rfhan=open(rfpath,'w')
    recrfhd={'Ftype': 'Run', 'Rtype': 'HD','Prgnm':prgnm,'NIN':nin,'NOUT':nout}
    s=str(recrfhd)
    rfhan.write(s + '\n')
    i=0
    while i < int(nin)+ int(nout):
        if i < int(nin):
            recrfvl={'Rtype': 'IN','uval':rfuvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        else:
            recrfvl={'Rtype': 'OUT','uval':rfuvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        i=i+1
    recrfdep= {'Rtype': 'DEPTH','Type': dt,'Start': 'start','End': 'end'}
    s=str(recrfdep)
    rfhan.write(s + '\n')
    rfhan.close()
    
def fnm2num(curnode: str, rtype: str, fname: str, kind: str = '') -> str:
    """fnm2num."""
                # open s.0 for curnode
                # read records looking for match to file type and name
                # if present return num else
                # if EOF return ''
    if curnode[0] == '2':
        curpath = adnod.uns2path(curnode)
    else:
        curpath = adnod.ns2path(curnode)
    infpath = curpath+"/s.0"
    infhan=open(infpath,"r")
    for line in infhan.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if kind == '':
                if d['Rtype'] == rtype and d['Name']==fname :
                    fnum=d['FileNum']
                    infhan.close()
                    return fnum
            else:
                if d['Rtype'] == rtype and d['Name']==fname and d['Kind']== kind:
                    fnum=d['FileNum']
                    infhan.close()
                    return fnum
    infhan.close()
    fnum = ' '
    return fnum


# write user global file
def wruglobf(usernode: str, glfnam: str, glnams: list[str], glvals: list[str]) -> None:
    """wruglobf."""
    userpath = adnod.uns2path(usernode)
    sfn = fnm2num(usernode, 'SF', glfnam, "Glob")
    if sfn == ' ':
        uglpath, n = nxtsf(usernode)
        wrrecsf(userpath, str(n), glfnam, 'Glob')
    else:
        uglpath = userpath + r"/s."+sfn
    uglhan = open(uglpath, 'w')
    i = 0
    while i < len(glnams):
        recglvl = {'Rtype': 'Global','Glonam':glnams[i],'Gloval':glvals[i]}
        s = str(recglvl)
        uglhan.write(s + '\n')
        i = i+1
    uglhan.close()
    return


def rduglobf(usernode: str, glfnam: str, glnams: list[str], glvals: list[str]) -> None:
    """rduglobf."""
    userpath = adnod.uns2path(usernode)
    sfn = fnm2num(usernode, 'SF', glfnam, "Glob")
    if sfn == ' ':
        return
    else:
        uglpath = userpath + r"/s."+sfn
        uglhan = open(uglpath, 'r')
        for line in uglhan.readlines():
            line=line.strip("\n")
            if len(line)> 1 and line[0]== "{":
                d=ast.literal_eval(line) # line is now a dictionary
                i = 0
                while i < len(glnams):
                    if d['Glonam']== glnams[i]:
                        glvals[i] = d['Gloval']
                    i = i + 1
    uglhan.close()
    return


def rdnodesf(usernode: str, nodesfnam: str, nodes: list[str], nodenames: list[str]) -> None:
    """rdnodesf."""
    userpath = adnod.uns2path(usernode)
    sfn = fnm2num(usernode, 'SF', nodesfnam, "Nodes")
    if sfn == ' ':
        return
    else:
        nodespath = userpath + r"/s."+sfn
        nodeshan = open(nodespath, 'r')
        for line in nodeshan.readlines():
            line = line.strip("\n")
            if len(line) > 1 and line[0] == "{":
                d = ast.literal_eval(line)  # line is now a dictionary
                nodes.append(d['NStr'])
                nodenames.append(d['NNam'])
        nodeshan. close()
    return

# write user nodes file


def wrnodesf(usernode: str, nodesfnam: str, nodes: list[str], nodenames: list[str]) -> None:
    """wrnodesf."""
    userpath = adnod.uns2path(usernode)
    sfn = fnm2num(usernode, 'SF', nodesfnam, "Nodes")
    if sfn == ' ':
        nodespath, n = nxtsf(usernode)
        wrrecsf(userpath, str(n), nodesfnam, 'Nodes')
    else:
        nodespath = userpath + r"/s."+sfn
    nodeshan = open(nodespath, 'w')
    i = 0
    while i < len(nodes):
        recnodes = {'NStr': nodes[i], 'NNam': nodenames[i]}
        s = str(recnodes)
        nodeshan.write(s + '\n')
        i = i+1
    nodeshan.close()
    return

def main() -> None:
    """Entry point for manual testing of pdh_files helpers."""
    print("pdh_files module loaded")


if __name__ == '__main__':
    main()

def unm2uns(username: str) -> str:
    """unm2uns."""
    urrpath = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../','USER','L1K1','L2K'))
    uns = ''
    i = 4
    urpath = urrpath + str(i) + r'\s.0'
    while os.path.exists(urpath):
        uh = open(urpath, 'r')
        for line in uh.readlines():
            line = line.strip("\n")
            if len(line) > 1 and line[0] == "{":
                d = ast.literal_eval(line)  # line is now a dictionary
                if d['Name'] == username:
                    uns = "2:1:" + str(i)
                    uh.close()
                    return uns
        i = i+1
        urpath = urrpath + str(i) + r'\s.0'
    return uns
def prnm2spath(progname: str) -> str:
    """prnm2spath."""
    prrpath = r'C:\PDH\System\L1K1\L2K'
    progspath=" "
    i = 1
    prpath = prrpath + str(i) + r'\s.0'
    while os.path.exists(prpath):
        ph = open(prpath, 'r')
        line = ph.readline()
        d = ast.literal_eval(line)  # line is now a dictionary
        if d['Prgnm'] == progname:
            print("Found Program")
            ph.close()
            progspath= prrpath + str(i) + r'\s.1'
            return progspath
        ph.close
        i = i+1
        prpath = prrpath + str(i) + r'\s.0'
    return progspath
