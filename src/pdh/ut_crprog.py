# create program entry
import os
import ast
progname = input('Enter New Program Name: 8 chars or less')
prrpath = r'C:\PDH\System\L1K1\L2K'
i = 1
prpath = prrpath + str(i) + r'\s.0'
while os.path.exists(prpath):
    ph = open(prpath, 'r')
    line = ph.readline()
    d = ast.literal_eval(line)  # line is now a dictionary
    if d['Prgnm'] == progname:
        print("Program already exists")
        ph.close()
        exit()
    ph.close
    i = i+1
    prpath = prrpath + str(i) + r'\s.0'
os.mkdir(prrpath + str(i))
desc = input('Enter Short Description for Program')
ph = open(prpath, 'w')
rec = {'Rtype': 'HD', 'Prgnm': progname, 'Desc': desc}
s = str(rec)
ph.write(s + "\n")
print("NewProgram: " + progname + " is Program # " + str(i))
ph.close()
