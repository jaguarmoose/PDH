"""Create a program entry in the System tree."""
import os
import ast


def create_program_entry(progname: str, desc: str, system_root: str = r"C:\PDH\System\L1K1\L2K") -> int:
    """Create a program record and return the program index used."""
    i = 1
    prpath = system_root + str(i) + r"\s.0"
    while os.path.exists(prpath):
        with open(prpath, "r") as ph:
            line = ph.readline()
            d = ast.literal_eval(line)  # line is now a dictionary
            if d["Prgnm"] == progname:
                raise ValueError("Program already exists")
        i += 1
        prpath = system_root + str(i) + r"\s.0"

    os.mkdir(system_root + str(i))
    with open(prpath, "w") as ph:
        rec = {"Rtype": "HD", "Prgnm": progname, "Desc": desc}
        ph.write(str(rec) + "\n")
    return i


def main() -> None:
    """Prompt for inputs and create a program entry."""
    progname = input("Enter New Program Name: 8 chars or less")
    desc = input("Enter Short Description for Program")
    try:
        idx = create_program_entry(progname, desc)
    except ValueError as exc:
        print(exc)
        return
    print("NewProgram: " + progname + " is Program # " + str(idx))


if __name__ == "__main__":
    main()
