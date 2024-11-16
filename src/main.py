"""A remake of the Google Play built-in Whirlybird game, which has appeares to
have disappeared from many Android devices for an unknown reason.
"""

from os import chdir, getcwd
from pathlib import Path
from sys import executable
import sys

from whirlybird_app import WhirlybirdApp

if __name__ == '__main__':
    old_cwd: str = getcwd()
    chdir(
        Path(executable).parent / '_internal'
        if getattr(sys, 'frozen', False)
        else Path(__file__).parent.parent
    )
    WhirlybirdApp().run()
    chdir(old_cwd)
