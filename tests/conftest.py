import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PYTHON_DIR = os.path.join(ROOT_DIR, "Development", "PYTHON")
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)
