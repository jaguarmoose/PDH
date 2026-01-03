import os
import subprocess
import sys

from pdh import adnod
from pdh import pdh_files


def run_cli():
    print(
        "Front End Commands:\n"
        "  ! execute a program (system tree)\n"
        "  + execute a user command file\n"
        "  - execute a global command file (User 0)\n"
        "  : execute a front end command\n"
        "  $ set or unset a global parameter\n"
        "  # move to a new interactive menu\n"
    )
    fec = input("Enter Front End Command")
    if not fec:
        return
    if fec[0] == "!":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, ".Archived_Code", "ip_rev1.py")
        env = os.environ.copy()
        src_dir = os.path.dirname(script_dir)
        env["PYTHONPATH"] = os.pathsep.join(
            [src_dir, env.get("PYTHONPATH", "")]
        ).strip(os.pathsep)
        subprocess.run([sys.executable, script_path], check=True, env=env)


def run_gui():
    from pdh.frend_gui import run_gui as _run_gui
    _run_gui()


if __name__ == "__main__":
    try:
        run_gui()
    except Exception:
        run_cli()
