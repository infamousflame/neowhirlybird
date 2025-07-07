"""Set everything up."""

from os import chdir, getcwd
from pathlib import Path
from sys import executable
import sys

from src.whirlybird_app import WhirlybirdApp

def main() -> int:
    """
    Change the current working directory to the package root before running the
    game and then change it back to what it was before.

    This is needed because the app is distributed as a single file, and the
    config file is not in the same directory as the app when it is run.
    """
    old_wd: str = getcwd()
    try:
        chdir(
            Path(executable).parent / '_internal'
            if getattr(sys, 'frozen', False)
            else Path(__file__).parent.parent
        )
        WhirlybirdApp().run()
    except Exception as e:
        print(e)
        return 1
    finally:
        # This always runs, even if a return statement is reached before.
        chdir(old_wd)
    return 0
