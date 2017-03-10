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
    #lasfnm = r"C:/PDH/Development/LAS/LAS Files/D-D' LAS Files/Bean/Bean_A.las"
    lasfnm="C:\PDH\Development\LAS\LAS Files\KGS-Cimarex\KGS-Cimarex.las"
else:
    lasfnm = input("Enter LAS File Name")

# Enter Parent Node string
pns="1:1:4"
# assume 1 file / well
curnode = adnod.nxtkid(pns)
def iterExample():
    for i in range(10):
        yield i

print(next(iterExample()))
lashan = open(lasfnm, 'r')
try:
    #deque(parseLAS(file))
    parsedLAS = parseLAS(lashan)
    curves = []
    cunits = []
    for line in parsedLAS:
        block,parsedLine = line
        if block == 'ascii':
            #print(curves)
            #print(block,parsedLine,line)
            curveMatrix = zip(*map(operator.itemgetter(1), itertools.chain((line,),parsedLAS)))
            #print('\n'.join(map(str, curveMatrix)))
            break
        elif block == 'curve':
            curve, unit, api_code, description = parsedLine
            #print(block,parsedLine,line)
            curves.append(curve)
            cunits.append(unit)
        #print('\n'.join(map(str, parseLAS(lashan))))
except LASParseError as e:
    print(e,filepath)
print("Here")
print(len(curves))
curveData = list(curveMatrix)
print(curves[0])
#for element in curveMatrix:
#    print(element)
#print(list(map(operator.itemgetter(1),curveData)))
test = [
[1, 2, 3],
[4, 5, 6],
[7, 8, 9]
]
print(test)
print(list(zip(*test)))
print(list(zip(test[0],test[1],test[2])))
depths = curveData[0]
# # determine Start Depth DI and End Depth assumes Depth is first curve and
# assumes Depth increase and there is more than 1 value of Depth
di = float(depths[1]) - float(depths[0])
sdi = str(di)
print(sdi)
label = "well_name_" + curnode
iname = "Depth"
units = "Feet"
si = depths[0]
nind = int((float(depths[-1]) - float(depths[0]))/di + 1)
snind = str(nind)
print(depths[0], depths[-1], sdi)
print(snind)
stuff = pdh_files.crinf(curnode, label, iname, units, si, snind, sdi)
units = "not yet"
icnm = 0
vpath = []
curpath = adnod.ns2path(curnode)
fv = []
ftmp = []
iv = 0
# created all new files - NOT MERGING - just write the rectangle of data
for cnm in curves:
    v = pdh_files.crvf(curnode, cnm, units, snind)
    vpath.append(curpath + r'/v.' + v)
    f = open(vpath[iv], 'w')
    fv.append(f)
    iv = iv+1
print(vpath)
sinx = 1
ninx = 1
minx = nind
ic = 0
for vf in fv:
    ix = 0
    while ix < nind:
        vf.write(curveData[ic][ix] + '\n')
        ix = ix + 1
    ic = ic + 1
for vf in fv:
    vf.close()
print("End")
