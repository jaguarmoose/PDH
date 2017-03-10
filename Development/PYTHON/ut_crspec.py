# create program spec file
import os
import ast
progname = input('Enter Program Name')
prrpath = r'C:\PDH\System\L1K1\L2K'
i = 1
prpath = prrpath + str(i) + r'\s.0'
while os.path.exists(prpath):
    ph = open(prpath, 'r')
    line = ph.readline()
    d = ast.literal_eval(line)  # line is now a dictionary
    if d['Prgnm'] == progname:
        print("Found Program ")
        ph.close()
        rec={ 'FileNum': '1', 'Name': progname, 'Rtype': 'SF', 'Kind': 'Spec'}
        s = str(rec)
        ph = open(prpath, 'a')
        ph.write(s + "\n")
        ph.close()
        # now find ask for input and ouputs then specifics for each
        # open s.0 file - put entry in s.0 and finish spec file
        # and s.1
        p0=open(prrpath + str(i)+ r'\s.1','w')
        nin = input('Number of inputs :')
        nout = input('Number of outputs :')
        rec={'Ftype': 'Spec', 'Rtype': 'HD','Prgnm':progname,'NIN':nin,'NOUT':nout}
        s = str(rec)
        p0.write(s + "\n")
        j=0
        while j < int(nin):
            lab = input('Enter Label for Input #: '+ str(j))
            defl = input('Enter default for Input #: '+ str(j))
            units = input('Enter units for Input #: '+ str(j))
            helpt = input('Enter help for Input #: '+ str(j))
            rec={'Rtype':'IN','NUM':str(j),'label': lab,'def': defl,'units': units,'help': helpt,'range':''}
            s = str(rec)
            p0.write(s + "\n")
            j=j+1
        j=0
        while j <  int(nout):
            lab = input('Enter Label for Output #: '+ str(j))
            defl = input('Enter default for Output #:'+ str(j))
            units = input('Enter units for Output #: '+ str(j))
            helpt = input('Enter help for Output #: '+ str(j))

            rec={'Rtype':'OUT','NUM':str(j),'label': lab,'def': defl,'units': units,'help': helpt,'range':''}
            s = str(rec)
            p0.write(s + "\n")
            j=j+1
        p0.close()    
        exit()
    ph.close()
    i = i+1
    prpath = prrpath + str(i) + r'\s.0'
