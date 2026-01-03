import os
import subprocess
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


COMMAND_HELP = [
    ("!", "execute a program (system tree)"),
    ("+", "execute a user command file"),
    ("-", "execute a global command file (User 0)"),
    (":", "execute a front end command"),
    ("$", "set or unset a global parameter"),
    ("#", "move to a new interactive menu"),
]


class FrendWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDH Front End")
        self.resize(640, 420)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Available Front End Commands"))

        self.command_list = QListWidget()
        for key, desc in COMMAND_HELP:
            QListWidgetItem(f"{key}  {desc}", self.command_list)
        layout.addWidget(self.command_list)

        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Command"))
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter Front End Command")
        input_row.addWidget(self.command_input)
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.handle_run)
        input_row.addWidget(self.run_button)
        layout.addLayout(input_row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def handle_run(self):
        fec = self.command_input.text().strip()
        if not fec:
            QMessageBox.information(self, "PDH Front End", "Enter a command.")
            return

        if fec[0] == "!":
            self.run_input_processor()
        else:
            self.output.append(f"Command received: {fec}")
            self.output.append("No handler implemented for this command yet.")

    def run_input_processor(self):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(package_dir, ".Archived_Code", "ip_rev1.py")
        if not os.path.exists(script_path):
            QMessageBox.warning(
                self,
                "PDH Front End",
                f"Missing script: {script_path}",
            )
            return

        try:
            env = os.environ.copy()
            src_dir = os.path.dirname(package_dir)
            env["PYTHONPATH"] = os.pathsep.join(
                [src_dir, env.get("PYTHONPATH", "")]
            ).strip(os.pathsep)
            result = subprocess.run(
                [sys.executable, script_path],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            if result.stdout:
                self.output.append(result.stdout.strip())
            if result.stderr:
                self.output.append(result.stderr.strip())
        except subprocess.CalledProcessError as exc:
            self.output.append(f"Error running ip_rev1.py: {exc}")
            if exc.stderr:
                self.output.append(exc.stderr.strip())


def run_gui():
    app = QApplication(sys.argv)
    window = FrendWindow()
    window.show()
    sys.exit(app.exec_())
