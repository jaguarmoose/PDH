# list programs program entry
import os
import ast
prrpath = r'C:\PDH\System\L1K1\L2K'
i = 1
prpath = prrpath + str(i) + r'\s.0'
while os.path.exists(prpath):
    ph = open(prpath, 'r')
    line = ph.readline()
    d = ast.literal_eval(line)  # line is now a dictionary
    progname = d['Prgnm']
    desc = d['Desc']
    print('Program #' + str(i) + ' Name: ' + progname + '  Description: ' + desc)
    ph.close
    i = i+1
    prpath = prrpath + str(i) + r'\s.0'
