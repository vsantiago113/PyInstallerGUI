# PyInstallerGUI

PyInstallerGUI is a user interface for PyInstaller, a program that freezes (packages) Python programs into stand-alone executables, under Windows, Linux, Mac OS X, FreeBSD, Solaris and AIX. The interface lets you select the options, select the directory and files and with a click of a button it execute the commands in the shell. You can add icons to your executable, version files and also extract the version file from other executable files.

How to download and use:

Download the GUI from GITHUB under releases.
Extract the package, then run the command "pip install -r requirements.txt" to install PyInstaller, future and Pillow or install them manually using pip.
When you run the GUI and select a file and don't change any options by default is going to create the program in console, and all the data and dependencies in a single directory and the executable will have the PyInstaller icon. If you want to create an executable of a GUI program, for example, an application developed using Tkinter then you have to select --Windowed or the command prompt will show up when you run the program. You can create a single executable file by clicking check on --onefile. A single file has all the data and dependencies packed into itself. If you already have a version file, you can select the file and check the option --version-file. If you need to create one you can go on Tools -> GrabVersion and if you are in Windows, for example, you can go to C:\Windows and select notepad.exe to extract the notepad.exe version file. Then you can modify this version file and while you are creating the executable or after by going to Tools -> SetVersion. You can have the executable have any icon you like by selecting the --icon option. If you are in Windows, you must create the image in the .ico format. PyInstaller supports UPX to pack the executable and make the size smaller, check out UPX at https://upx.github.io/.



Important: if you have directories with images, other executables or files, after you compile your code into an executable you must copy these folders back to the root of your program where the executable is. For example, if in the root of your application you have a directory named images with icons and other images when you turn your code into an executable PyInstaller does not move these automatically, so you will have to do that manually. You must copy the folder images to the root where you have your executable.



The PyInstaller GUI was only tested in Windows using Python versions 2 and 3.

To learn more about Pyinstaller check out their documentation the PyInstaller Manual at https://pyinstaller.readthedocs.io/en/stable/.
