"""Create a user entry in the User tree."""
import os
import ast

from pdh import pdh_files
from pdh import adnod


def create_user(username: str, user_root: str = r"C:\PDH\USER\L1K1\L2K") -> int:
    """Create a new user node and return the user index."""
    i = 1
    urpath = user_root + str(i) + r"\s.0"
    while os.path.exists(urpath):
        with open(urpath, "r") as uh:
            line = uh.readline()
            d = ast.literal_eval(line)  # line is now a dictionary
            if d["Name"] == username:
                raise ValueError("User already exists")
        i += 1
        urpath = user_root + str(i) + r"\s.0"

    os.mkdir(user_root + str(i))
    with open(urpath, "w") as uh:
        rec = {"Rtype": "HD", "Ftype": "Info_User", "Name": username}
        uh.write(str(rec) + "\n")
    return i


def main() -> None:
    """Prompt for a username and create the user record."""
    username = input("Enter User Name")
    try:
        idx = create_user(username)
    except ValueError as exc:
        print(exc)
        return
    print("New User: " + username + " is User # " + str(idx))


if __name__ == "__main__":
    main()
