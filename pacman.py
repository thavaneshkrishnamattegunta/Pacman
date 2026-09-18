"""Root launcher for the Pacman game.

Run `python pacman.py` from the Pacman folder to start the random-map game.
All command-line arguments are forwarded to pacman_search/pacman.py.
"""
import os
import runpy
import sys


PROJECT_DIR = os.path.join(os.path.dirname(__file__), "pacman_search")
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)
runpy.run_path(os.path.join(PROJECT_DIR, "pacman.py"), run_name="__main__")
