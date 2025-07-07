linux_from_linux:
	python3 -m PyInstaller spec/pyinstaller.spec

windows_from_linux:
	wine python -m PyInstaller spec/pyinstaller.spec

windows_from_windows:
	python -m PyInstaller spec/pyinstaller.spec

android_from_linux:
	python3 -m buildozer --version
	cp spec/buildozer.spec buildozer.spec
	python3 -m buildozer -v android debug
	rm buildozer.spec
