def adnod(ns):      # Add a data node to 
    import os
    path = ns2path(ns)
    os.mkdir(path)  # need to do a whole bunch of error checking
    path=path+"\s.0"
    fs0=open(path,"w")
    fs0.close
def ns2path(ns):    # convert a nodestring to dir path
    import os
    path='C:\PDH\DATA'
    nanc= ns.split(":")
    nlev = len(nanc)
    for I in range(1,nlev):
        path = path + "\L" + str(I)+ "K"+ nanc[I]
    print(path)
    return path
def uns2path(uns,urpath):    # convert a user number to dir path
    import os
    nanc= ns.split(":")
    nlev = len(nanc)
    for I in range(1,nlev):
        path = urpath + "\L" + str(I)+ "K"+ nanc[I]
    print(path)
    return path
            
