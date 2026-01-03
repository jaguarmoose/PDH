"""List program entries from the System tree."""
import os
import ast
from typing import Iterator


def iter_programs(system_root: str) -> Iterator[tuple[int, str, str]]:
    """Yield (index, name, desc) entries from the program records."""
    i = 1
    prpath = os.path.join(system_root + str(i), "s.0")
    while os.path.isfile(prpath):
        with open(prpath, "r") as ph:
            line = ph.readline()
            d = ast.literal_eval(line)  # line is now a dictionary
            yield i, d["Prgnm"], d["Desc"]
        i += 1
        prpath = os.path.join(system_root + str(i), "s.0")


def main() -> None:
    """Print program entries using a default root."""
    system_root = os.sep + os.path.join("Users", "robertfarnan", "PDH", "System", "L1K1", "L2K")
    for idx, progname, desc in iter_programs(system_root):
        print("Program #" + str(idx) + " Name: " + progname + "  Description: " + desc)


if __name__ == "__main__":
    main()
