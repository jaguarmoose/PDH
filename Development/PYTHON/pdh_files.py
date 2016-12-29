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

def crdi(path,label,npts,start,units):
    fo=open(path,"a")
    for line in fo.readlines():
         line=line.strip('\n')
         d={line}       
                      # if rectype = DI update those values 
         oline=line + "\n"
         fo.write(oline)
    
def crzf(ns,label):
    import os       
    import adnod
    path = adnod.ns2path(ns)
    zfpath,n=nxtsf(ns) # find next file name
    fs0=open(zfpath,"w")
    fs0.write(label+'\n')
    fs0.close
    path = adnod.ns2path(ns)
    path= path + "\s.0"
    fs0=open(path,"a")
    zf="ZF."+label+" "+str(n)
    fs0.write(zf+'\n')
    fs0.close
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
def crvf(ns, name, units,npts): #Create a Vector File, updated to include npts in call
    import os
    import ast
    import adnod
    nval= -999.99            # Null value written to all VFile on creation
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
    while index < npts: 
        fvf.write(str(nval)+ "\n")   # read DI record from INF get Sd,NPT,DI
        index=index+1
    fvf.close()              # write the new VF record to inf  
    return vpath;                        
def nxtvf(ns):    
    import os
    import adnod
    n=1
    rpath = adnod.ns2path(ns)
    path=rpath+r"\v."+str(n)
    while os.path.isfile(path):
        n=n+1
        path=rpath+r"\v."+str(n)
    return path,n

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

def wrgp(path,name,value,units):  # write a GP or update a GP in an INF file
    import os                   # within record find name replace value with value
    infile=path                 # if record not found append to file
    outfile=path+"tmp"
    fi=open(infile, 'r') # open file for reading
    fo=open(outfile,'a') # open file for appending
    for line in fi.readlines():
         line=line.strip('\n')
         d={line}
         rt=d['Rytpe']
         print (line, str(d))
         print (rt)
         oline=line + "\n"
         fo.write(oline)
    rec1={'Rtype':'GP','Name':'Rw','Value':".05",'Unit':'Ohm-m'}     
    s=str(rec1)
    fo.write(s+ "\n")
    fi.close()
    fo.close()
    os.remove(infile)
    os.rename(outfile,infile)

   
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
def rdrf(rfpath,rfhead,rfivals,rfovals,rfdepth):    
    import ast
    import sys
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
            
            elif d['Rtype'] == 'OUT':
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
def rdusrrf(urfpath,urfvals,urfdepths):
    import ast
    import sys
    urfhan=open(urfpath,'r') # Open User Run File 
    for line in urfhan.readlines():  
        line=line.strip("\n")
        if len(line)> 1 and line[0]== "{":
            d=ast.literal_eval(line) # line is now a dictionary
            if d['Rtype']== 'IN' or d['Rtype']== 'OUT': 
                urfvals.append(d['val']) #
            elif d['Rtype'] == 'DEPTH':
                urfdepths.append(d['TYPE'])
                urfdepths.append(d['Start'])
                urfdepths.append(d['End'])
    urfhan.close()
    return
def wrrf(rfpath,prgnm,nin,nout,rfvals,sindex,npts,mxpts):
    import sys
    rfhan=open(rfpath,'w')
    recrfhd={'Ftype': 'Run', 'Rtype': 'HD','Prgnm':prgnm,'NIN':nin,'NOUT':nout}
    s=str(recrfhd)
    rfhan.write(s + '\n')
    i=0
    while i < int(nin)+ int(nout):
        if i < int(nin):
            recrfvl={'Rtype': 'IN','val':rfvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        else:
            recrfvl={'Rtype': 'OUT','val':rfvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        i=i+1
    recrfdep= {'Rtype': 'DEPTH','Start': sindex,'NPTS': npts,'MXPTS': mxpts}
    s=str(recrfdep)
    rfhan.write(s + '\n')
    rfhan.close()
    return
def wrurf(rfpath,prgnm,nin,nout,rfvals,start,end):
    # biggest way this differs from runfile is depth is in DI units and curves GPs are named
    import sys
    rfhan=open(rfpath,'w')
    recrfhd={'Ftype': 'Run', 'Rtype': 'HD','Prgnm':prgnm,'NIN':nin,'NOUT':nout}
    s=str(recrfhd)
    rfhan.write(s + '\n')
    i=0
    while i < int(nin)+ int(nout):
        if i < int(nin):
            recrfvl={'Rtype': 'IN','val':rfvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        else:
            recrfvl={'Rtype': 'OUT','val':rfvals[i]}
            s=str(recrfvl)
            rfhan.write(s + '\n')
        i=i+1
    recrfdep= {'Rtype': 'DEPTH','Type':'','Start': start,'End': end}
    s=str(recrfdep)
    rfhan.write(s + '\n')
    rfhan.close()
    return
def vnm2num(curnode,vfname):
                # open s.0 for curnode
                # read vf records looking for vfname if present return VF#
                # if EOF return ''
    return            
def gp2val(curnode,newval):    # gp to value
    return

def zp2val(curnode,zone,newval): # zone parm to value
    return
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






