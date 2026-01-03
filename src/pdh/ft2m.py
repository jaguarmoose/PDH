from tkinter import *
from tkinter import ttk


def build_ui(root: Tk) -> tuple[StringVar, StringVar]:
    """Create the feet-to-meters UI and return (feet_var, meters_var)."""
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    feet = StringVar()
    meters = StringVar()

    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=2, row=1, sticky=(W, E))

    ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(mainframe, text="Calculate", command=lambda: calculate(feet, meters)).grid(
        column=3, row=3, sticky=W
    )

    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    feet_entry.focus()
    root.bind("<Return>", lambda _event: calculate(feet, meters))
    return feet, meters


def calculate(feet_var: StringVar, meters_var: StringVar) -> None:
    """Calculate meters from feet input."""
    try:
        value = float(feet_var.get())
        meters_var.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


def main() -> None:
    """Launch the feet-to-meters GUI."""
    root = Tk()
    root.title("Feet to Meters")
    build_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
