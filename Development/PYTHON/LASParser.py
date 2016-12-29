import re, itertools

def getSection(match):
    return {
        'A':'ascii',
        'C':'curve',
        'V':'version',
        'W':'well'
    }[match]

parameterRule = re.compile(u'([^\.]*)\.([^\s]*)\s*([^:]*):([^\n]*)')

#Version 2.0+
#STRT.FT                                      100.0000:
def parseLAS(lines):

    sep = None
    currentSection = None
    version = None
    for i,line in enumerate(lines):
        if line.strip().startswith('~'):
            try:
                currentSection = getSection(line.strip()[1:2].upper())
            except:
                print('bad ascii block',line)
                return
            if currentSection == 'ascii':
                break
        if line.strip().startswith('#'):
            yield('comment',line)
        elif currentSection != 'ascii'
            match = parameterRule.match(line)
            if match:
                parameter,unit,value,description = match.groups()
                yield(currentSection,(parameter,unit,value,description))
        else:
            break
    #handle ascii block
    for line in lines:
        yield (currentSection,line.split())

if __name__ == '__main__':
    lasfnm = u"C:\PDH\Development\LAS\LAS Files\D-D' LAS Files\Bean\Bean_A.las"

    lashan=open(lasfnm,'r')
    try:
        print('\n'.join(map(str,parseLAS(lashan))))

    except:
        print('issue parsing')
