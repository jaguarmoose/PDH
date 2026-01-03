import os

def adnod(ns):
    """Add a child node directory and create its s.0 file."""
    path = ns2path(ns)
    os.mkdir(path)  # need to do a whole bunch of error checking
    path = os.path.join(path, "s.0")
    with open(path, "w"):
        pass

def nxtkid(pns):
    """Return the next available child node and create its directory."""
    i=1
    kns=pns+":"+str(i)
    path = ns2path(kns)
    while os.path.exists(path):
        i=i+1
        kns=pns+":"+str(i)
        path=ns2path(kns)
    os.mkdir(path)
    return kns

def ns2path(ns):
    """Convert a node string to a data directory path."""
    path = r'C:\PDH\DATA'
    nanc= ns.split(":")
    nlev = len(nanc)
    for I in range(1,nlev):
        path = os.path.join(path, f"L{I}K{nanc[I]}")
    print(path)
    return path

def uns2path(uns):
    """Convert a user node string to a user directory path."""
    urpath = r'C:\PDH\USER'
    nanc= uns.split(":")
    nlev = len(nanc)
    for I in range(1,nlev):
        urpath = os.path.join(urpath, f"L{I}K{nanc[I]}")
    print(urpath)
    return urpath


def main():
    """Run a simple node conversion example."""
    ns2path("1:1")


if __name__ == "__main__":
    main()
