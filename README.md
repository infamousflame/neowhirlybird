# neowhirlybird
A remake of the Google Play built-in Whirlybird game, which has appeares to
have disappeared from many Android devices for an unknown reason.

## Installation

This app is designed to work on multiple platforms, though it works much
better on some devices than others. I am limited in the number of platforms I
can compile for, so binary distributions do not cover everything, and you may
need to consider building it yourself.

### Building from source

This project's license permits you to build it yourself from this source code
(or a modified version), and distribute that as well. This also allows you to
get it to work on a platform I have not provided an official build for.

You can build it with whatever works, but I have provided spec files for
[Buildozer](https://github.com/kivy/buildozer) and
[PyInstaller](https://pyinstaller.org/). You can use these to get started.

### Binaries from GitHub

If available, you can also download my official binaries right here on GitHub.
As I mentioned earlier, these are not available on all platforms. Make sure
you download the correct version for your device.

## Playing the Game

For those who are new to Whirlybird, welcome! The game's pretty
straightforward - move left and right, using the A/D keys on the keyboard or 
tilting a device about its vertical (y) axis - to bounce off platforms and
avoid the spikes.

For those already familiar with the Google game, there are some things to
note: Tilting the device works well, but often you may find that it does not
return to stationary when tilted back. There are also some issues if the
device is rotated in other ways, such as when in a turning vehicle. I am still
working on a fix for these issues.

I am also exploring additional ways to control the game on a wider range of
devices.

## Missing features

This is a project I'm working on in my spare time, and as such, development
might be a bit slow.
In saying that, development is progressing much faster than I expected, but
there are some notable features of the original game still absent:
* Sounds
* Animations
* High score display - currently as I develop it, the difficulty changes a
lot, so this will not be added until I have finished balancing everything out.

## License Information

This project makes use of the [Kivy](https://kivy.org/) framework (Copyright
(c) 2010-2024 Kivy Team and other contributors) and its dependencies (each
with their respective copyright holder). Both this code and Kivy are
distributed under the MIT License. Please see here for
[license information for Kivy's dependencies](https://kivy.org/doc/stable/guide/licensing.html).

