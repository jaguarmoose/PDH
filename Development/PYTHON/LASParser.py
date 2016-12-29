import re
import os
import sys
import traceback
from collections import deque


def getSection(match):
    return {
        'A': 'ascii',
        'C': 'curve',
        'V': 'version',
        'W': 'well',
        'P': 'parameter',
        'O': 'other'
    }[match]


parameterRule = re.compile(u'([^\.]*)\.([^\s]*)\s*([^:]*):([^\n]*)')

# Version 2.0+
# STRT.FT                                      100.0000:


def parseLAS(lines):
    sep = None
    version = None
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
                print('unknown block', line)
                return
        if line.strip().startswith('#') or currentSection == 'other':
            yield('comment', line)
        elif currentSection != 'ascii':
            match = parameterRule.match(line)
            if match:
                parameter, unit, value, description = map(str.strip, match.groups())
                if version < 2:
                    value, description = description, value
                if currentSection == 'version':
                    if parameter.upper() == 'WRAP':
                        wrap = value
                    elif parameter.upper() == 'VERS':
                        try:
                            version = float(value)
                        except:
                            version = value
                    elif parameter.upper() == 'SEP':
                        sep = value
                elif currentSection == 'well':
                    if parameter.upper() == 'STRT':
                        strt = value
                    elif parameter.upper() == 'STOP':
                        stop = value
                    elif parameter.upper() == 'STEP':
                        step = value
                    elif parameter.upper() == 'NULL':
                        null = value
                elif currentSection == 'curve':
                    curves.append(parameter.strip())
                yield(currentSection, (parameter, unit, value, description))
        else:
            # handle ascii block
            firstLine = True
            for i, line in enumerate(lines, i):
                if sep is None:
                    values = line.split()
                else:
                    values = line.split(sep)
                if len(values) != len(curves):
                    print('Mismatch Length of curves and values', curves, values, line)
                    raise LASParseError("Mismatch Length of Curves: {} and Values: {} for Line#: {}".format(stop, values[0], curves[0], line))
                else:
                    if firstLine:
                        firstLine = False
                        if float(strt) != float(values[0]):
                            if float(stop) == float(values[0]):
                                raise LASParseError("Stop Value: {} matches First Value: {} in Reference: {} for Line#: {}".format(stop, values[0], curves[0], line))
                            else:
                                raise LASParseError("Start Value: {} does not match First Value: {} in Reference: {} for Line#: {}".format(strt, values[0], curves[0], line))
                yield (currentSection, values)

            if float(stop) != float(values[0]):
                raise LASParseError("Stop Value: {} does not match Last Value: {} in Reference: {} for Line#: {}".format(stop, values[0], curves[0], line))

class LASParseError(Exception):
    pass


if __name__ == '__main__':
    folderPath = os.path.realpath(os.path.join("Development", "LAS",
                                               "LAS Files"))

    for root, dirs, files in os.walk(folderPath, topdown=False):
        for filename in files:
            if filename.lower().endswith('.las'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    try:
                        deque(parseLAS(file))
                        # print('\n'.join(map(str, parseLAS(lashan))))
                    except LASParseError as e:
                        print(e,filepath)
                        # exc_type, exc_obj, tb = sys.exc_info()
                        # f = tb.tb_frame
                        # lineno = tb.tb_lineno
                        # python_filename = f.f_code.co_filename
                        # print 'EXCEPTION {}, FILE {}, {}'.format(type(e).__name__,filepath, e)
