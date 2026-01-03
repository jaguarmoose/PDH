from pdh.las_parser import parse_las, LASParseError
import itertools
import operator
from typing import Iterator

from pdh import adnod
from pdh import pdh_files


def iter_example() -> Iterator[int]:
    """Yield a few example integers for quick sanity checks."""
    for i in range(10):
        yield i


def parse_las_to_node(lasfnm: str, parent_node: str = "1:1:4") -> str | None:
    """Parse a LAS file and write curves into a new child node."""
    curnode = adnod.nxtkid(parent_node)
    with open(lasfnm, "r") as lashan:
        try:
            parsedLAS = parse_las(lashan)
            curves = []
            cunits = []
            for line in parsedLAS:
                block, parsedLine = line
                if block == "ascii":
                    curveMatrix = zip(
                        *map(operator.itemgetter(1), itertools.chain((line,), parsedLAS))
                    )
                    break
                elif block == "curve":
                    curve, unit, api_code, description = parsedLine
                    curves.append(curve)
                    cunits.append(unit)
        except LASParseError as exc:
            print(exc, lasfnm)
            return None

    curveData = list(curveMatrix)
    depths = curveData[0]
    di = float(depths[1]) - float(depths[0])
    sdi = str(di)
    label = "well_name_" + curnode
    iname = "Depth"
    units = "Feet"
    si = depths[0]
    nind = int((float(depths[-1]) - float(depths[0])) / di + 1)
    snind = str(nind)

    pdh_files.crinf(curnode, label, iname, units, si, snind, sdi)
    curpath = adnod.ns2path(curnode)

    vpath = []
    fv = []
    iv = 0
    for cnm in curves:
        v = pdh_files.crvf(curnode, cnm, units, snind)
        vpath.append(curpath + r"/v." + v)
        f = open(vpath[iv], "w")
        fv.append(f)
        iv += 1

    ic = 0
    for vf in fv:
        ix = 0
        while ix < nind:
            vf.write(curveData[ic][ix] + "\n")
            ix += 1
        ic += 1
    for vf in fv:
        vf.close()
    return curnode


def main(lasfnm: str | None = None, parent_node: str = "1:1:4") -> None:
    """Run the LAS parser-to-node workflow with defaults."""
    if lasfnm is None:
        lasfnm = r"C:/PDH/Development/LAS/LAS Files/D-D' LAS Files/Bean/Bean_A.las"
    print(next(iter_example()))
    parse_las_to_node(lasfnm, parent_node=parent_node)


if __name__ == "__main__":
    main()
