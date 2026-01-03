"""Create a program spec file."""
import os
import ast


def _prompt_specs(kind: str, count: int | str) -> list[dict[str, str]]:
    """_prompt_specs."""
    items = []
    j = 0
    while j < int(count):
        lab = input(f"Enter Label for {kind} # {j}")
        defl = input(f"Enter default for {kind} # {j}")
        units = input(f"Enter units for {kind} # {j}")
        helpt = input(f"Enter help for {kind} # {j}")
        items.append(
            {
                "Rtype": kind.upper(),
                "NUM": str(j),
                "label": lab,
                "def": defl,
                "units": units,
                "help": helpt,
                "range": "",
            }
        )
        j += 1
    return items


def create_program_spec(
    progname: str,
    nin: int | str,
    nout: int | str,
    inputs: list[dict[str, str]] | None = None,
    outputs: list[dict[str, str]] | None = None,
    system_root: str = r"C:\PDH\System\L1K1\L2K",
) -> str:
    """Create a spec file for an existing program."""
    i = 1
    prpath = system_root + str(i) + r"\s.0"
    while os.path.exists(prpath):
        with open(prpath, "r") as ph:
            line = ph.readline()
            d = ast.literal_eval(line)  # line is now a dictionary
            if d["Prgnm"] == progname:
                rec = {"FileNum": "1", "Name": progname, "Rtype": "SF", "Kind": "Spec"}
                with open(prpath, "a") as wh:
                    wh.write(str(rec) + "\n")
                spec_path = system_root + str(i) + r"\s.1"
                with open(spec_path, "w") as p0:
                    header = {"Ftype": "Spec", "Rtype": "HD", "Prgnm": progname, "NIN": str(nin), "NOUT": str(nout)}
                    p0.write(str(header) + "\n")
                    for rec in inputs or []:
                        p0.write(str(rec) + "\n")
                    for rec in outputs or []:
                        p0.write(str(rec) + "\n")
                return spec_path
        i += 1
        prpath = system_root + str(i) + r"\s.0"
    raise FileNotFoundError("Program not found")


def main() -> None:
    """Prompt for program spec inputs and write the spec file."""
    progname = input("Enter Program Name")
    nin = input("Number of inputs :")
    nout = input("Number of outputs :")
    inputs = _prompt_specs("input", nin)
    outputs = _prompt_specs("output", nout)
    try:
        spec_path = create_program_spec(progname, nin, nout, inputs=inputs, outputs=outputs)
    except FileNotFoundError as exc:
        print(exc)
        return
    print("Wrote spec file at " + spec_path)


if __name__ == "__main__":
    main()
