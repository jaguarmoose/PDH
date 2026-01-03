# create user
import os
from pdh import pdh_files
import ast
from pdh import adnod
username = input('Enter User Name')      # Add a data node to
urrpath = r'C:\PDH\USER\L1K1\L2K'
i = 1
urpath = urrpath + str(i) + r'\s.0'
while os.path.exists(urpath):
    uh = open(urpath, 'r')
    line = uh.readline()
    d = ast.literal_eval(line)  # line is now a dictionary
    if d['Name'] == username:
        print ("User already exists")
        uh.close()
        exit()
    uh.close
    i = i+1
    urpath = urrpath + str(i) + r'\s.0'
os.mkdir(urrpath + str(i))    
uh = open(urpath,'w')
rec = {'Rtype': 'HD', 'Ftype': 'Info_User','Name': username}
s = str(rec)
uh.write(s + "\n")
print ("New User: " + username + " is User # " + str(i))
uh.close()
