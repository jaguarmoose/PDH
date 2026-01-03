import argparse

from pdh import frend


def main():
    parser = argparse.ArgumentParser(description="PDH front end")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run the CLI front end instead of the GUI",
    )
    args = parser.parse_args()

    if args.cli:
        frend.run_cli()
    else:
        try:
            frend.run_gui()
        except Exception:
            frend.run_cli()


if __name__ == "__main__":
    main()
