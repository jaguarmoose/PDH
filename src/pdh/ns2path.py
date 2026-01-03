import os


def adnod(ns: str, data_root: str = r"C:\PDH\DATA") -> None:
    """Add a data node directory for the given node string."""
    path = ns2path(ns, data_root=data_root)
    os.mkdir(path)  # need to do a whole bunch of error checking


def ns2path(ns: str, data_root: str = r"C:\PDH\DATA") -> str:
    """Convert a node string to a directory path."""
    path = data_root
    nanc = ns.split(":")
    nlev = len(nanc)
    for i in range(1, nlev):
        path = path + "\\L" + str(i) + "K" + nanc[i]
    print(path)
    return path


def main() -> None:
    """Run a simple conversion example."""
    ns2path("1:1")


if __name__ == "__main__":
    main()
            
