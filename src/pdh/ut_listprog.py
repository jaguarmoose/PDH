''' list programs program entry '''
import os
import ast
prrpath = os.sep+os.path.join('Users', 'robertfarnan', 'PDH', 'System', 'L1K1', 'L2K')
i = 1
prpath = os.path.join(prrpath + str(i), 's.0')
while os.path.isfile(prpath):
    with open(prpath, 'r') as ph:
        line = ph.readline()
        d = ast.literal_eval(line)  # line is now a dictionary
        progname = d['Prgnm']
        desc = d['Desc']
        print('Program #' + str(i) + ' Name: ' + progname + '  Description: ' + desc)

    i = i+1
    prpath = os.path.join(prrpath + str(i), 's.0')
