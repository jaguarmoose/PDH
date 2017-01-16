def adnod(ns):      # Add a kid node -given parent node - this creates system folder
    import os
    path = ns2path(ns)
    os.mkdir(path)  # need to do a whole bunch of error checking
    path=path+"\s.0"
    fs0=open(path,"w")
    fs0.close
# Add a kid node -given parent node - this creates system folder
def nxtkid(pns):
    import os
    i=1
    kns=pns+":"+str(i)
    path = ns2path(kns)
    while os.path.exists(path):
        i=i+1
        kns=pns+":"+str(i)
        path=ns2path(kns)
    os.mkdir(path)
    return kns

def ns2path(ns):    # convert a nodestring to dir path
    import os
    path='C:\PDH\DATA'
    nanc= ns.split(":")
    nlev = len(nanc)
    for I in range(1,nlev):
        path = path + "\L" + str(I)+ "K"+ nanc[I]
    print(path)
    return path
def un2path(uns,urpath):    # convert a user number to dir path
    import os
    nanc= ns.split(":")
    nlev = len(nanc)
    for I in range(1,nlev):
        path = urpath + "\L" + str(I)+ "K"+ nanc[I]
    print(path)
    return path
