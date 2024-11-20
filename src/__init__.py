"""Set everything up."""

from os import chdir, getcwd
from pathlib import Path
from sys import executable
import sys

from src.whirlybird_app import WhirlybirdApp

def main() -> None:
    old_cwd: str = getcwd()
    chdir(
        Path(executable).parent / '_internal'
        if getattr(sys, 'frozen', False)
        else Path(__file__).parent.parent
    )
    WhirlybirdApp().run()
    chdir(old_cwd)
