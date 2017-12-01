__author__      = 'Victor Santiago'
__copyright__   = 'Copyright (C) 2014, Victor Santiago'
__credits__     = 'Victor Santiago'
__license__     = 'GNU GPL v2.0'
__version__     = '1.0.0.0'
__maintainer__  = 'Victor Santiago'
__email__       = 'vsantiago@vs113dev.com'
__status__      = 'Beta'

# PyInstaller GUI Dependencies:
# The Libraries below are required for PyInstaller GUI to run.
    # pywin32: http://sourceforge.net/projects/pywin32/
    # Pillow(PIL): https://pypi.python.org/pypi/Pillow

# The library below is already part of PyInstaller GUI but I got it from the link below.
# http://stackoverflow.com/questions/14267900/python-drag-and-drop-explorer-files-to-tkinter-entry-widget

import Tkinter as tk
import ttk, win32api, urllib2, tkFileDialog, os, webbrowser, win32clipboard, win32con
import tkFont as font
import tkMessageBox as messagebox
try:
    # For Pillow: This is the new version of PIL.
    from PIL import Image, ImageTk, ImageOps
except ImportError:
    try:
        # For PIL: This is the old version of PIL I recommend that you use Pillow.
        import Image, ImageTk, ImageOps
    except ImportError as ex:
        print 'Please download Pillow or PIL'
        print ex
os.environ['TKDND_LIBRARY'] = 'modules/tkdnd2.6/'
from modules.untested_tkdnd_wrapper import TkDND

COLOR='#E0E0DA'

class MainApp:
    def __init__(self, parent, dnd):

        def CheckUpdate():
            try:
                data = urllib2.urlopen('http://vs113dev.com/projects/pyinstallergui/version.txt').read()
                if str(data) > str(__version__):
                    messagebox.showinfo('Software Update','Update Available!')
                else:
                    messagebox.showinfo('Software Update','No Updates are Available.')
            except Exception as ex:
                print ex
                messagebox.showinfo('Software Update','Unable to Check for Update ')

        def AboutMe():
            CallDisplayAboutMe = DisplayAboutMe(parent)

        def CallSetVersion():
            CallSetVersionFile = SetVersionFile(parent, dnd)

        def CallGrabVersion():
            CallGrabVersionFile = GrabVersionFile(parent, dnd)

        def OpenWebsite():
            link = 'http://www.pyinstaller.org/export/v2.0/project/doc/Manual.html'
            webbrowser.open_new_tab(link)

        def DownloadPyInstaller():
            link = 'https://github.com/pyinstaller/pyinstaller'
            webbrowser.open_new_tab(link)

        def DownloadUPX():
            link = 'http://upx.sourceforge.net'
            webbrowser.open_new_tab(link)

        def CommandInfo(string):
            if string == 'onefile':
                messagebox.showinfo('Info','Create a single file deployment')
            elif string == 'name':
                messagebox.showinfo('Info','Optional name to assign to the project (from which the spec file name is generated). If omitted, the basename of the (first) script is used.')
            elif string == 'subsystem':
                messagebox.showinfo('Info','Use a console subsystem executable (default) or use a windowed subsystem executable, which on Windows does not open the console when the program is launched')
            elif string == 'noupx':
                messagebox.showinfo('Info','Do not use UPX even if available (works differently between Windows and *nix)')
            elif string == 'versionfile':
                messagebox.showinfo('Info','Add a version resource from FILE to the exe')
            elif string == 'icon':
                messagebox.showinfo('Info','If FILE is an .ico file, add the icon to the final executable.')

        def GetDirectoryString(string):
            if string == 'versionfile':
                filename = tkFileDialog.askopenfilename(filetypes = [('Version File', '*.txt')])
                entry2.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry2.insert(tk.END, str(filename))
            elif string == 'script':
                filename = tkFileDialog.askopenfilename(filetypes = [('Python Script', '*.py | *.pyw')])
                entry3.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry3.insert(tk.END, str(filename))
            elif string == 'icon':
                filename = tkFileDialog.askopenfilename(filetypes = [('Icon', '*.ico')])
                entry4.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry4.insert(tk.END, str(filename))

            BuildCommand('')

        def BuildCommand(event):
            string = 'PyInstaller\\pyinstaller.py'+self.ComboBoxVar1.get()+self.CheckBoxVar2.get()+self.CheckBoxVar3.get()
            if self.CheckBoxVar1.get() == '' or entry1.get().strip() == '':
               pass
            else:
                string += self.CheckBoxVar1.get()+'="'+entry1.get().strip()+'"'
            if self.CheckBoxVar4.get() == '' or entry2.get().strip() == '':
                pass
            else:
                string += self.CheckBoxVar4.get()+'="'+entry2.get().strip()+'"'
            if entry3.get().strip() == '':
                pass
            else:
                string += ' "'+entry3.get()+'"'
            if self.CheckBoxVar5.get() == '' or entry4.get().strip() == '':
                pass
            else:
                string += self.CheckBoxVar5.get()+' "'+entry4.get()+'"'
                
            entry5.delete(0, tk.END)
            entry5.insert(tk.END, string)

        def RunBuild():
            if entry3.get().strip() == '':
                pass
            else:
                os.system(str(entry5.get().strip()))
                self.ComboBoxVar1.set(' --console')
                self.CheckBoxVar1.set('')
                entry1.delete(0, tk.END)
                self.CheckBoxVar2.set('')
                self.CheckBoxVar3.set(' --noupx')
                self.CheckBoxVar4.set('')
                entry2.delete(0, tk.END)
                entry3.delete(0, tk.END)
                self.CheckBoxVar5.set('')
                entry4.delete(0, tk.END)
                BuildCommand('')

        def dnd_handle(event):
            event.widget.delete(0, tk.END)
            event.widget.insert(tk.END, event.data.strip('{').strip('}'))
            BuildCommand('')

        def CopyToClipboard():
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, entry5.get().strip())
            win32clipboard.CloseClipboard()
            
        menubar = tk.Menu(parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=parent.destroy)
        menubar.add_cascade(label='File', menu=filemenu)

        toolsmenu = tk.Menu(menubar, tearoff=0)
        toolsmenu.add_command(label='SetVersion', command=CallSetVersion)
        toolsmenu.add_command(label='GrabVersion', command=CallGrabVersion)
        menubar.add_cascade(label='Tools', menu=toolsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='PyInstaller Manual', command=OpenWebsite)
        helpmenu.add_command(label='PyInstaller Develop Download', command=DownloadPyInstaller)
        helpmenu.add_command(label='UPX Download', command=DownloadUPX)
        helpmenu.add_command(label='Check for updates', command=CheckUpdate)
        helpmenu.add_command(label='About', command=AboutMe)
        menubar.add_cascade(label='Help', menu=helpmenu)

        parent.config(menu=menubar)

        self.logoImage = ImageTk.PhotoImage(Image.open('images/logo.png'))
        label1 = tk.Label(parent, image=self.logoImage); label1.pack(side=tk.TOP)    

        self.ComboBoxVar1 = tk.StringVar()
        self.ComboBoxVar1.set(' --console')
        ComboBox1 = ttk.Combobox(parent, values=[' --console',' --windowed'], textvariable=self.ComboBoxVar1, state='readonly')
        ComboBox1.place(width=143, height=21, x=10, y=124)
        ComboBox1.bind('<<ComboboxSelected>>', BuildCommand)

        button1 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('subsystem')); button1.place(width=40, height=25, x=163, y=124)

        self.CheckBoxVar1 = tk.StringVar()
        self.CheckBoxVar1.set('')
        CheckBox1 = ttk.Checkbutton(parent, text=('--name')
                                    ,variable=self.CheckBoxVar1, onvalue=' --name', offvalue='', command=lambda: BuildCommand('')); CheckBox1.place(width=63, height=21, x=245, y=124)
        entry1 = ttk.Entry(parent); entry1.place(width=126, height=21, x=318, y=124)
        
        button2 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('name')); button2.place(width=40, height=25, x=454, y=124)

        self.CheckBoxVar2 = tk.StringVar()
        self.CheckBoxVar2.set('')
        CheckBox2 = ttk.Checkbutton(parent, text='--onefile',
                                 variable=self.CheckBoxVar2, onvalue=' --onefile', offvalue='', command=lambda: BuildCommand('')); CheckBox2.place(width=69, height=21, x=10, y=159)
        button3 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('onefile')); button3.place(width=40, height=25, x=89, y=159)

        self.CheckBoxVar3 = tk.StringVar()
        self.CheckBoxVar3.set(' --noupx')
        CheckBox3 = ttk.Checkbutton(parent, text=('--noupx')
                                    ,variable=self.CheckBoxVar3, onvalue=' --noupx', offvalue='', command=lambda: BuildCommand('')); CheckBox3.place(width=66, height=21, x=164, y=159)

        button4 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('noupx')); button4.place(width=40, height=25, x=240, y=159)

        self.CheckBoxVar4 = tk.StringVar()
        self.CheckBoxVar4.set('')
        CheckBox4 = ttk.Checkbutton(parent, text='--version-file',
                                 variable=self.CheckBoxVar4, onvalue=' --version-file', offvalue='', command=lambda: BuildCommand('')); CheckBox4.place(width=92, height=21, x=10, y=194)
        
        button5 = ttk.Button(parent, text='Browse', command=lambda: GetDirectoryString('versionfile')); button5.place(width=76, height=25, x=112, y=194)

        entry2 = ttk.Entry(parent); entry2.place(width=248, height=21, x=198, y=197)
        dnd.bindtarget(entry2, dnd_handle, 'text/uri-list')

        button6 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('versionfile')); button6.place(width=40, height=25, x=456, y=194)

        label2 = tk.Label(parent, text='Script', bg=COLOR); label2.place(width=36, height=21, x=10, y=229)
        button7 = ttk.Button(parent, text='Browse', command=lambda: GetDirectoryString('script')); button7.place(width=76, height=25, x=56, y=229)
        entry3 = ttk.Entry(parent); entry3.place(width=354, height=21, x=142, y=229)
        dnd.bindtarget(entry3, dnd_handle, 'text/uri-list')

        self.CheckBoxVar5 = tk.StringVar()
        self.CheckBoxVar5.set('')
        CheckBox5 = ttk.Checkbutton(parent, text='--icon',
                                 variable=self.CheckBoxVar5, onvalue=' --icon', offvalue='', command=lambda: BuildCommand('')); CheckBox5.place(width=56, height=21, x=10, y=264)
        button8 = ttk.Button(parent, text='Browse', command=lambda: GetDirectoryString('icon')); button8.place(width=76, height=25, x=76, y=264)
        entry4 = ttk.Entry(parent); entry4.place(width=284, height=21, x=162, y=264)
        dnd.bindtarget(entry4, dnd_handle, 'text/uri-list')
        button9 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('icon')); button9.place(width=40, height=25, x=456, y=264)

        label3 = tk.Label(parent, text='Command', bg=COLOR); label3.place(width=63, height=21, x=10, y=299)
        entry5 = ttk.Entry(parent); entry5.place(width=363, height=21, x=83, y=299)
        button6 = ttk.Button(parent, text='Copy', width=5, command=CopyToClipboard); button6.place(width=40, height=25, x=456, y=299)
        BuildCommand('')
        
        button10 = ttk.Button(parent, text='Build', command=RunBuild); button10.place(width=76, height=25, x=(506/2)-86, y=340)
        button11 = ttk.Button(parent, text='Close', command=parent.destroy); button11.place(width=76, height=25, x=(506/2)+10, y=340)

        ttk.Style().configure('TCheckbutton', background=COLOR)

class DisplayAboutMe(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        
        self.transient(parent)
        self.result = None
        self.grab_set()
        wFilter = 300; hFilter = 310
        w = wFilter - 15; h = hFilter - 37
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.geometry('{0}x{1}+{2}+{3}'.format(w, h, int(x), int(y)))
        self.resizable(width=False, height=False)
        self.title('About')
        self.wm_iconbitmap('images/python.ico')

        self.image = Image.open('images/vs.png')
        self.size = (100, 100)
        self.thumb = ImageOps.fit(self.image, self.size, Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.thumb)
        logoLabel = tk.Label(self, image=self.photo); logoLabel.pack(side=tk.TOP, pady=10)

        f1 = tk.Frame(self); f1.pack()
        f2 = tk.Frame(self); f2.pack(pady=10)
        f3 = tk.Frame(f2); f3.pack()

        def CallHyperLink(EventArgs):
            webbrowser.get('windows-default').open_new_tab('www.vs113dev.com')

        tk.Label(f1, text='PyInstaller GUI '+str(__version__)).pack()
        tk.Label(f1, text='Copyright (C) 2014 Victor Santiago').pack()
        tk.Label(f1, text='All rights reserved').pack()

        f = font.Font(size=10, slant='italic', underline=True)
        label1 = tk.Label(f3, text='www.vs113dev.com', font = f, cursor='hand2')
        label1['foreground'] = 'blue'
        label1.pack(side=tk.LEFT)
        label1.bind('<Button-1>', CallHyperLink)
        ttk.Button(self, text='OK', command=self.destroy).pack(pady=5)

class SetVersionFile(tk.Toplevel):
    def __init__(self, parent, dnd):
        tk.Toplevel.__init__(self, parent)
        
        self.transient(parent)
        self.result = None
        self.grab_set()
        w = 506; h = 300
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.geometry('{0}x{1}+{2}+{3}'.format(w, h, int(x), int(y)))
        self.resizable(width=False, height=False)
        self.configure(background=COLOR)
        self.title('Set Version File')
        self.wm_iconbitmap('images/python.ico')

        def dnd_handle(event):
            event.widget.delete(0, tk.END)
            event.widget.insert(tk.END, event.data.strip('{').strip('}'))
            GetDirectoryString('')

        def GetDirectoryString(string):
            if string == 'fileversion':
                filename = tkFileDialog.askopenfilename(filetypes = [('Version File', '*.txt')])
                entry1.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry1.insert(tk.END, str(filename))
            elif string == 'executable':
                filename = tkFileDialog.askopenfilename(filetypes = [('Executable', '*.exe')])
                entry2.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry2.insert(tk.END, str(filename))

            entry3.delete(0, tk.END)
            string = r'PyInstaller\utils\set_version.py'
            if str(entry1.get().strip()) == '':
                pass
            else:
                string += ' "'+str(entry1.get())+'"'
            if str(entry2.get().strip()) == '':
                pass
            else:
                string += ' "'+str(entry2.get())+'"'
            entry3.insert(tk.END, string)

        self.logoImage = ImageTk.PhotoImage(Image.open('images/logo.png'))
        label1 = tk.Label(self, image=self.logoImage); label1.pack(side=tk.TOP)

        def SetVersion():
            os.system(r'PyInstaller\utils\set_version.py "'+str(entry1.get().strip())+'" "'+str(entry2.get().strip())+'"')
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry3.insert(tk.END, r'PyInstaller\utils\set_version.py')

        def CopyToClipboard():
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, entry3.get().strip())
            win32clipboard.CloseClipboard()

        label2 = tk.Label(self, text='File Version', bg=COLOR); label2.place(x=10, y=120)
        button1 = ttk.Button(self, text='Browse', command=lambda: GetDirectoryString('fileversion'))
        button1.place(x=80, y=120)
        entry1 = ttk.Entry(self); entry1.place(width=506-76-100, height=21, x=165, y=122)
        dnd.bindtarget(entry1, dnd_handle, 'text/uri-list')

        label3 = tk.Label(self, text='Executable', bg=COLOR); label3.place(x=10, y=155)
        button2 = ttk.Button(self, text='Browse', command=lambda: GetDirectoryString('executable'))
        button2.place(x=80, y=155)
        entry2 = ttk.Entry(self); entry2.place(width=330, height=21, x=165, y=157)
        dnd.bindtarget(entry2, dnd_handle, 'text/uri-list')

        label4 = tk.Label(self, text='Command', bg=COLOR); label4.place(x=10, y=192)
        entry3 = ttk.Entry(self); entry3.place(width=365, height=21, x=80, y=192)
        entry3.insert(tk.END, r'PyInstaller\utils\set_version.py')
        button3 = ttk.Button(self, text='Copy', width=5, command=CopyToClipboard); button3.place(width=40, height=25, x=456, y=192)

        button4 = ttk.Button(self, text='Set Version', command=SetVersion); button4.place(width=76, height=25, x=(506/2)-86, y=235)
        button5 = ttk.Button(self, text='Close', command=self.destroy); button5.place(width=76, height=25, x=(506/2)+10, y=235)

class GrabVersionFile(tk.Toplevel):
    def __init__(self, parent, dnd):
        tk.Toplevel.__init__(self, parent)
        
        self.transient(parent)
        self.result = None
        self.grab_set()
        w = 506; h = 230
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.geometry('{0}x{1}+{2}+{3}'.format(w, h, int(x), int(y)))
        self.resizable(width=False, height=False)
        self.configure(background=COLOR)
        self.title('Set Version File')
        self.wm_iconbitmap('images/python.ico')

        def dnd_handle(event):
            event.widget.delete(0, tk.END)
            event.widget.insert(tk.END, event.data.strip('{').strip('}'))
            GetDirectoryString('')

        def GetDirectoryString(string):
            if string == 'executable':
                filename = tkFileDialog.askopenfilename(filetypes = [('Executable', '*.exe')])
                entry1.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry1.insert(tk.END, str(filename))

            entry2.delete(0, tk.END)
            string = r'PyInstaller\utils\grab_version.py'
            if str(entry1.get().strip()) == '':
                pass
            else:
                string += ' "'+str(entry1.get())+'"'
            entry2.insert(tk.END, string)

        self.logoImage = ImageTk.PhotoImage(Image.open('images/logo.png'))
        label1 = tk.Label(self, image=self.logoImage); label1.pack(side=tk.TOP)

        def GrabVersion():
            string = r'PyInstaller\utils\grab_version.py "'+str(entry1.get().strip())+'"'
            os.system(string)
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry2.insert(tk.END, r'PyInstaller\utils\grab_version.py')

        def CopyToClipboard():
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, entry2.get().strip())
            win32clipboard.CloseClipboard()

        label2 = tk.Label(self, text='Executable', bg=COLOR); label2.place(x=10, y=120)
        button1 = ttk.Button(self, text='Browse', command=lambda: GetDirectoryString('executable'))
        button1.place(x=80, y=120)
        entry1 = ttk.Entry(self); entry1.place(width=506-76-100, height=21, x=165, y=122)
        dnd.bindtarget(entry1, dnd_handle, 'text/uri-list')

        label3 = tk.Label(self, text='Command', bg=COLOR); label3.place(x=10, y=155)
        entry2 = ttk.Entry(self); entry2.place(width=365, height=21, x=80, y=155)
        entry2.insert(tk.END, r'PyInstaller\utils\grab_version.py')
        button2 = ttk.Button(self, text='Copy', width=5, command=CopyToClipboard); button2.place(width=40, height=25, x=456, y=155)

        button3 = ttk.Button(self, text='Grab Version', command=GrabVersion); button3.place(width=76, height=25, x=(506/2)-86, y=190)
        button4 = ttk.Button(self, text='Close', command=self.destroy); button4.place(width=76, height=25, x=(506/2)+10, y=190)


def main():
    root = tk.Tk()
    root.geometry('506x400')
    root.resizable(False, False)
    root.title('PyInstaller GUI Version: '+str(__version__))
    root.wm_iconbitmap('images/python.ico')
    root.configure(background=COLOR)
    dnd = TkDND(root)
    CallMainApp = MainApp(root, dnd)
    root.mainloop()

if __name__ == '__main__':
    main()
