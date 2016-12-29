import re
from collections import deque


def getSection(match):
    return {
        'A': 'ascii',
        'C': 'curve',
        'V': 'version',
        'W': 'well'
    }[match]


parameterRule = re.compile(u'([^\.]*)\.([^\s]*)\s*([^:]*):([^\n]*)')

# Version 2.0+
# STRT.FT                                      100.0000:


def parseLAS(lines):
    sep = None
    wrap = None
    strt = None
    stop = None
    step = None
    null = None
    curves = []
    currentSection = None
    version = None
    for i, line in enumerate(lines):
        if line.strip().startswith('~'):
            try:
                currentSection = getSection(line.strip()[1:2].upper())
            except:
                print('bad ascii block', line)
                return
            if currentSection == 'ascii':
                break
        if line.strip().startswith('#'):
            yield('comment', line)
        elif currentSection != 'ascii':
            match = parameterRule.match(line)
            if match:
                parameter, unit, value, description = match.groups()
                if currentSection == 'version':
                    if parameter.upper() == 'WRAP':
                        wrap = value.strip().lower()
                    elif parameter.upper() == 'SEP':
                        sep = value.strip().lower()
                elif currentSection == 'curve':
                    curves.append(parameter.strip())
                yield(currentSection, (parameter, unit, value, description))
        else:
            break
    # handle ascii block
    for line in lines:
        values = line.split()
        if len(values) < len(curves):
            print('Mismatch Length of curves and values', curves, values, line)
        yield (currentSection, values)


if __name__ == '__main__':
    lasfnm = u"C:\PDH\Development\LAS\LAS Files\D-D' LAS Files\Bean\Bean_A.las"

    lashan = open(lasfnm, 'r')
    try:
        deque(parseLAS(lashan))
        # print('\n'.join(map(str, parseLAS(lashan))))
    except Exception as e:
        print('issue parsing', e)
