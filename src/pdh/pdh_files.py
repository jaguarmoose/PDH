import ast
import os
import sys

from pdh import adnod

# Create an info file given a NodeString
# Need to error check for directory and file then return
def crinf(ns,label,iname,units,si,npts,di): # Nodestring and Node Label
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
def rdinf(ns): #,nodename,nindex,nstart,nnpts,ndi,nunits): # returns a list
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

def crdi(path,label,npts,start,units):
    fo=open(path,"a")
    for line in fo.readlines():
         line=line.strip('\n')
         d={line}
                      # if rectype = DI update those values
         oline=line + "\n"
         fo.write(oline)
def rdzone (curnode,zname): # Looks for Zone-zname in INF returns ztop zbase or ' '
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
def wrzone(curnode,zonenm,ztop,zbase):
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
def wrzp(curnode,zonenm,zpname,zpvalue,zpunits=' '):
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


def rdzp(curnode,zonenm,zpname):
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
def nxtsf(ns):
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
def crvf(ns, name, units,npts, nval=-999.99):
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
def nxtvf(ns):
    n=1
    rpath = adnod.ns2path(ns)
    path=rpath+r"\v."+str(n)
    while os.path.isfile(path):
        n=n+1
        path=rpath+r"\v."+str(n)
    return path,str(n)

def upsf(path): # open file path look record begin with rlab
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
def rdgp(curnode,gpname):
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

def wrgp(path,name,value,units):  # write a GP or update a GP in an INF file
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

def wrrecvf(path,n,name,units):
    finf=open(path+"s.0","a")
    recvf={'Rtype':'VF','Name': name,'FileNum': n,'Units':units}
    return
def wrrecsf(path,n,name,kind=''):
    finf=open(path+"\s.0","a")
    recsf=str({'Rtype':'SF','Name': name,'FileNum': n,'Kind':kind})
    oline=recsf + "\n"
    finf.write(oline)
    finf.close()
    fsf=open(path +"s."+n,'w')
    fsf.write(str({'Rtype':'HD','Name': name})+'\n')
    fsf.close()
    return
def upvf(vpath,sinx,ninx,minx,vdata):     # This will write to a vector file
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


def rdrf(rfpath, rfhead, rfuivals,rfivals,rfuovals, rfovals, rfdepth):

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
def rdspecf(sppath,sphead,sptypr,splabs,spdef,spunits,sphelp,sprng):
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
def rdusrrf(urfpath,urfuvals,dt):
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
def wrrf(rfpath,prgnm,nin,nout,rfuvals,rfvals,sindex,npts,mxpts):
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
def wrurf(rfpath,prgnm,nin,nout,rfuvals,dt):
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
    
def fnm2num(curnode,rtype,fname,kind=''):
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
def wruglobf(usernode, glfnam, glnams, glvals):
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


def rduglobf(usernode, glfnam, glnams, glvals):
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


def rdnodesf(usernode, nodesfnam, nodes, nodenames):
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


def wrnodesf(usernode, nodesfnam, nodes, nodenames):
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

def main():
    """Entry point for manual testing of pdh_files helpers."""
    print("pdh_files module loaded")


if __name__ == '__main__':
    main()

def unm2uns(username):    # convert user name to user number
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
def prnm2spath(progname): #program name to program number
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
