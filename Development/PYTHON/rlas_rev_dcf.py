from LASParser import parseLAS, LASParseError
import sys
import getopt
import adnod
import pdh_files
import os
import itertools
import operator

# input file name
# input output node address
# Should nodes even have an address, or should the folder name indicate
# address?
# node guid folders
# assume 1 file / well

# open LAS file
# call parseLASFile()
# for each line in parseLASFile
#   output properties to properties
#   output curves to curves

if __name__ == '__main__':
    curnode = "1:1:4:1"  # frend provides curnode working in 1:4 for test
    lasfnm = r"C:/PDH/Development/LAS/LAS Files/D-D' LAS Files/Bean/Bean_A.las"
                                           
else:
    lasfnm = input("Enter LAS File Name")

lashan = open(lasfnm, 'r')
try:
    #deque(parseLAS(file))
    parsedLAS = parseLAS(lashan)
    curves = []
    for line in parsedLAS:
        if line[0] == 'ascii':
            print(curves)
            curveMatrix = zip(*map(operator.itemgetter(1), itertools.chain((line,),parsedLAS)))
            #print('\n'.join(map(str, curveMatrix)))
            break
        elif line[0] == 'curve':
            #print(line)
            curves.append(line[1][0])

    # print('\n'.join(map(str, parseLAS(lashan))))
except LASParseError as e:
    print(e,filepath)

# line=''
# while line[0:2]!='~A':
#    print(line[0:2])
#    line=lashan.readline()
# print('here')
# line=line.strip("\n")
# cnames=line.split()
# cnames.pop(0)   # removes leading ~A from list
# # should be a curve data start line now split names
# ncurves=len(cnames)    # Splits
# # build
# # determine Start Depth DI and End Depth
# # Read still EOF
# line=lashan.readline()
# line=line.strip("\n")
# cvals=line.split()
# sdepth=cvals[0]
# line=lashan.readline()
# line=line.strip("\n")
# cvals=line.split()
# sdepth2=cvals[0]
# sdi=str(float(sdepth2)-float(sdepth))
# ndeps=2
# while line !=''and line !=' ' :
#    line=lashan.readline()
#    ndeps=ndeps+1
#    cvals=line.split()
#    if len(cvals)> 0:
#        edepth=cvals[0]
#   # print (edepth)
# lashan.close()
# label="well_name_"+curnode
# iname="Depth"
# units="Feet"
# si=sdepth
# snind=str(ndeps)
# di=sdi
# stuff=pdh_files.crinf(curnode,label,iname,units,si,snind,di)# INF create
# units="not yet"
# icnm=0
# vpath=[]
# fv=[]
# ftmp=[]
# iv=0
# for cnm in cnames:
#    v = pdh_files.crvf(curnode, cnm, units,ndeps)
#    vpath.append(v)
#    f=open(vpath[iv],'r')
#    fv.append(f)
#    ft=open(vpath[iv] + r"_tmp",'w')
#    ftmp.append(ft)
#    iv=iv+1
# sinx=1
# ninx=1
# minx=ndeps
# lashan=open(lasfnm,'r')
# line=' '
# ic=0
# #Startswith
# while line[0:2]!='~A':
#    line=lashan.readline()
# while line !=''and line !=' ' :
#    line=lashan.readline()
#    cvals=line.split()
#    if len(cvals)> 0 and ic < minx:
#        ic=ic+1
#                    # first loop until start index
#        if ic < sinx or ic > sinx+minx-1 :   # and loop after end index
#            ir=0
#            for vf in fv:
#                dum=vf.readline()
#                dum=dum.strip('\n')
#                ftmp[ir].write(dum+'\n')
#                ir=ir+1
#        else:                          # In indexes that need calculation
#            icv=0
#            ir=0
# #for vf,tvf in fv,ftmp:
#            for vf in fv:
#                dum=vf.readline()
#                ftmp[ir].write(cvals[icv]+'\n')
#                icv=icv+1
#                ir=ir+1
# for vf in fv:
#    vf.close()
# for tvf in ftmp:
#    tvf.close()
# for vp in vpath:
#    os.remove(vp)
#    os.rename(vp +r"_tmp",vp)
# print ("End")
