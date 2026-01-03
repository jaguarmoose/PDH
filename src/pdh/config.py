"""Configure PDH folder paths."""
import configparser
import os


def load_paths(config_path: str | None = None, base_path: str | None = None) -> dict[str, str]:
    """Load configured paths and return a dict of resolved directories."""
    if base_path is None:
        base_path = os.path.realpath(os.path.join(__file__, "..", "..", ".."))
    if config_path is None:
        config_path = os.path.join(base_path, "pdh.cfg")

    config = configparser.RawConfigParser()
    config.read(config_path)

    return {
        "pdh": base_path,
        "user": os.path.join(base_path, config.get("PDH", "path_user")),
        "system": os.path.join(base_path, config.get("PDH", "path_system")),
        "data": os.path.join(base_path, config.get("PDH", "path_data")),
    }


def main() -> None:
    """Print configured path availability using default config."""
    paths = load_paths()
    for label, path in (("USER", paths["user"]), ("SYSTEM", paths["system"]), ("DATA", paths["data"])):
        if os.path.isdir(path):
            print(label + " Path: " + path)
        else:
            print("**Missing** " + label + " Path: " + path)


if __name__ == "__main__":
    main()
