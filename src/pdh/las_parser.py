'''Old LAS Parser'''

import re
import os
from collections import deque


def getSection(match):
    '''get section name from first Upper character'''
    return {
        'A': 'ascii',
        'C': 'curve',
        'V': 'version',
        'W': 'well',
        'P': 'parameter',
        'O': 'other'
    }[match]


__ParameterRule__ = re.compile(r'([^\.]*)\.([^\s]*)\s*([^:]*):([^\n]*)')


def parseLAS(lines):
    '''Pass in raw las file lines'''
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

        # Check for Section Delimiter Character ~
        if line.strip().startswith('~'):
            try:
                currentSection = getSection(line.strip()[1:2].upper())
            except:
                raise LASParseError(
                    "Unknown Section: {} at Line#: {}".format(line.strip(), i))
        if line.strip().startswith('#') or currentSection == 'other':
            yield('comment', line)
        elif currentSection != 'ascii':
            match = parameterRule.match(line)
            if match:
                # Split common line format into pieces and clean
                parameter, unit, value, description = map(
                    str.strip, match.groups())
                if version is not None and version < 2:
                    value, description = description, value
                if currentSection == 'version':
                    if parameter.upper() == 'WRAP':
                        wrap = value
                    elif parameter.upper() == 'VERS':
                        # Try to float value so we can compare it numerically
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
                    # build list so we can use these later
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
                    raise LASParseError("Mismatch Length of Curves: {} and Values: {} for Line#: {}".format(
                        values[0], curves[0], line))
                else:
                    if firstLine:
                        firstLine = False
                        if float(strt) != float(values[0]):
                            if float(stop) == float(values[0]):
                                raise LASParseError("Stop Value: {} matches First Value: {} in Reference: {} for Line#: {}".format(
                                    values[0], curves[0], line))
                            else:
                                raise LASParseError("Start Value: {} does not match First Value: {} in Reference: {} for Line#: {}".format(
                                    strt, values[0], curves[0], line))
                    yield (currentSection, values)

            if float(stop) != float(values[0]):
                raise LASParseError("Stop Value: {} does not match Last Value: {} in Reference: {} for Line#: {}".format(
                    stop, values[0], curves[0], line))


class LASParseError(Exception):
    pass


def validate_folder(folder_path=None):
    """Parse all LAS files under a folder and print any errors."""
    if folder_path is None:
        folder_path = os.path.realpath(os.path.join("Development", "LAS", "LAS Files"))

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for filename in files:
            if filename.lower().endswith(".las"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r") as las_file:
                    try:
                        deque(parseLAS(las_file))
                    except LASParseError as e:
                        print(e, filepath)


def main():
    """Validate LAS files using default folder location."""
    validate_folder()


if __name__ == "__main__":
    main()
