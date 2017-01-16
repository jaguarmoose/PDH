# Create an info file given a NodeString
# Need to error check for directory and file then return
def crinf(ns,label,iname,units,si,npts,di): # Nodestring and Node Label
    import os
    import adnod
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
    import os
    import adnod
    import ast
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
    import os ,ast ,adnod
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
    import os ,ast ,adnod
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
    import os ,ast,adnod                # within record find name replace value with value
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
    import ast, adnod               # within record find name replace value with value
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
    import os
    import adnod
    n=1
    path = adnod.ns2path(ns)
    path=path+"\s."+str(n)
    while os.path.isfile(path):
        n=n+1
        path=path+"\s."+str(n)
    return path,n
def crvf(ns, name, units,npts, nval=-999.99):
     #Create a Vector File, updated: include npts in call nval in call default
    import os
    import ast
    import adnod
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
    import os
    import adnod
    n=1
    rpath = adnod.ns2path(ns)
    path=rpath+r"\v."+str(n)
    while os.path.isfile(path):
        n=n+1
        path=rpath+r"\v."+str(n)
    return path,str(n)

def upsf(path): # open file path look record begin with rlab
    import os                   # within record find name replace value with value
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
    import os,ast,adnod
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
    import os ,ast                # within record find name replace value with value
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

def upvf(vpath,sinx,ninx,minx,vdata):     # This will write to a vector file
    import os
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

    import ast
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
    import ast
    import sys
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
def rdusrrf(urfpath,urfuvals):
    import ast
    import sys
    urfhan=open(urfpath,'r') # Open User Run File
    for line in urfhan.readlines():
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype']== 'IN' or d['Rtype']== 'OUT':
                urfuvals.append(d['uval']) #
            #elif d['Rtype'] == 'DEPTH':
            #    urfdepths.append(d['TYPE'])
            #    urfdepths.append(d['Start'])
            #    urfdepths.append(d['End'])
    urfhan.close()
    return
def wrrf(rfpath,prgnm,nin,nout,rfuvals,rfvals,sindex,npts,mxpts):
    import sys
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
def wrurf(rfpath,prgnm,nin,nout,rfuvals):
    # biggest way this differs from runfile is depth is in DI units and curves GPs are named
    import sys
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
#    recrfdep= {'Rtype': 'DEPTH','Type':'','Start': start,'End': end}
#    s=str(recrfdep)
    rfhan.write(s + '\n')
    rfhan.close()
    return
def vnm2num(curnode,vfname):
                # open s.0 for curnode
                # read vf records looking for vfname if present return VF#
                # if EOF return ''
    import os,ast,adnod
    curpath=adnod.ns2path(curnode)
    infpath=curpath+"/s.0"
    infhan=open(infpath,"r")
    for line in infhan.readlines():
        line=line.strip('\n')
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype'] =='VF' and d['Name']==vfname :
                vnum=d['FileNum']
                infhan.close()
                return vnum
    infhan.close()
    vnum=' '
    return vnum
def sfnm2num(curnode,sflabel):      # Read s.0 node find Sf label return file #
    return
def rduglobf(uffpath,ugnvals,ugfvals): # This still needs to be flanged out for all global names
    import ast
    import sys
    uffhan=open(uffpath,'r') # Open User Run File
    for line in uffhan.readlines():
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
#'Rtype':'GNode','Nodecrit':'','Curnode':'','Rfcon':'','Zone':''}
            if d['Rtype']== 'Gnode':
                ugnvals.append(d['Curnode']) #
                ugnvals.append(d['Nodecrit']) #
                ugnvals.append(d['Rfcon']) #
                ugnvals.append(d['Zone']) #
 #'GFrend','CURMENU':'','HELPLEV':'','LASTMLEV':'','MODE':'','NOABORT':'','NOPROMPT':'','TERMID':''}
            elif d['Rtype'] == 'GFrend':
                ugfvals.append(d['Curmenu'])
                ugfvals.append(d['Helplev'])
                ugfvals.append(d['Lastlev'])
    uffhan.close()
    return
