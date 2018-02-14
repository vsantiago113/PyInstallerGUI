__version__     = '1.0.0.2'

import sys

if sys.version_info.major == 3:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import font
    from tkinter import filedialog
elif sys.version_info.major == 2:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
    import tkFont as font
    import tkFileDialog as filedialog
else:
    print('Python version 2 or 3 is required!')
    sys.exit(1)

import os, webbrowser
from PIL import Image, ImageTk, ImageOps

COLOR='#E0E0DA'

class MainApp:
    def __init__(self, parent):

        def CallSetVersion():
            CallSetVersionFile = SetVersionFile(parent)

        def CallGrabVersion():
            CallGrabVersionFile = GrabVersionFile(parent)

        def DocumentationPyInstaller():
            link = 'https://pyinstaller.readthedocs.io/en/stable/'
            webbrowser.open_new_tab(link)

        def DownloadPyInstaller():
            link = 'http://www.pyinstaller.org/downloads.html'
            webbrowser.open_new_tab(link)

        def DownloadUPX():
            link = 'https://upx.github.io'
            webbrowser.open_new_tab(link)

        def CommandInfo(string):
            if string == 'onefile':
                messagebox.showinfo('Info', 'Create a single file deployment')
            elif string == 'name':
                messagebox.showinfo('Info', 'Optional name to assign to the project (from which the spec file name is '
                                            'generated). If omitted, the basename of the (first) script is used.')
            elif string == 'subsystem':
                messagebox.showinfo('Info', 'Use a console subsystem executable (default) or use a windowed subsystem '
                                            'executable, which on Windows does not open the console when the program '
                                            'is launched')
            elif string == 'noupx':
                messagebox.showinfo('Info', 'Do not use UPX even if available (works differently between Windows and '
                                            '*nix)')
            elif string == 'versionfile':
                messagebox.showinfo('Info', 'Add a version resource from FILE to the exe')
            elif string == 'icon':
                messagebox.showinfo('Info','If FILE is an .ico file, add the icon to the final executable.')

        def GetDirectoryString(string):
            if string == 'versionfile':
                filename = filedialog.askopenfilename(filetypes = [('Version File', '*.txt')])
                entry2.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry2.insert(tk.END, str(filename))
            elif string == 'script':
                filename = filedialog.askopenfilename(filetypes = [('Python Script', '*.py | *.pyw')])
                entry3.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry3.insert(tk.END, str(filename))
            elif string == 'icon':
                filename = filedialog.askopenfilename(filetypes = [('Icon', '*.ico')])
                entry4.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry4.insert(tk.END, str(filename))

            BuildCommand('')

        def BuildCommand(event):
            string = 'pyinstaller --clean '+self.ComboBoxVar1.get()+self.CheckBoxVar2.get()+self.CheckBoxVar3.get()
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
            
        menubar = tk.Menu(parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Exit', command=parent.destroy)
        menubar.add_cascade(label='File', menu=filemenu)

        toolsmenu = tk.Menu(menubar, tearoff=0)
        toolsmenu.add_command(label='SetVersion', command=CallSetVersion)
        toolsmenu.add_command(label='GrabVersion', command=CallGrabVersion)
        menubar.add_cascade(label='Tools', menu=toolsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='PyInstaller Documentation', command=DocumentationPyInstaller)
        helpmenu.add_command(label='PyInstaller Download', command=DownloadPyInstaller)
        helpmenu.add_command(label='UPX Download', command=DownloadUPX)
        menubar.add_cascade(label='Help', menu=helpmenu)

        parent.config(menu=menubar)

        self.logoImage = ImageTk.PhotoImage(Image.open('images/logo.png'))
        label1 = tk.Label(parent, image=self.logoImage)
        label1.pack(side=tk.TOP)

        self.ComboBoxVar1 = tk.StringVar()
        self.ComboBoxVar1.set(' --console')
        ComboBox1 = ttk.Combobox(parent, values=[' --console',' --windowed'], textvariable=self.ComboBoxVar1,
                                 state='readonly')
        ComboBox1.place(width=143, height=21, x=10, y=124)
        ComboBox1.bind('<<ComboboxSelected>>', BuildCommand)

        button1 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('subsystem'))
        button1.place(width=40, height=25, x=163, y=124)

        self.CheckBoxVar1 = tk.StringVar()
        self.CheckBoxVar1.set('')
        CheckBox1 = ttk.Checkbutton(parent, text='--name', variable=self.CheckBoxVar1, onvalue=' --name', offvalue='',
                                    command=lambda: BuildCommand(''))
        CheckBox1.place(width=63, height=21, x=245, y=124)
        entry1 = ttk.Entry(parent)
        entry1.place(width=126, height=21, x=318, y=124)
        
        button2 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('name'))
        button2.place(width=40, height=25, x=454, y=124)

        self.CheckBoxVar2 = tk.StringVar()
        self.CheckBoxVar2.set('')
        CheckBox2 = ttk.Checkbutton(parent, text='--onefile', variable=self.CheckBoxVar2, onvalue=' --onefile',
                                    offvalue='', command=lambda: BuildCommand(''))
        CheckBox2.place(width=69, height=21, x=10, y=159)
        button3 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('onefile'))
        button3.place(width=40, height=25, x=89, y=159)

        self.CheckBoxVar3 = tk.StringVar()
        self.CheckBoxVar3.set(' --noupx')
        CheckBox3 = ttk.Checkbutton(parent, text=('--noupx'), variable=self.CheckBoxVar3, onvalue=' --noupx',
                                    offvalue='', command=lambda: BuildCommand(''))
        CheckBox3.place(width=66, height=21, x=164, y=159)

        button4 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('noupx'))
        button4.place(width=40, height=25, x=240, y=159)

        self.CheckBoxVar4 = tk.StringVar()
        self.CheckBoxVar4.set('')
        CheckBox4 = ttk.Checkbutton(parent, text='--version-file', variable=self.CheckBoxVar4,
                                    onvalue=' --version-file', offvalue='', command=lambda: BuildCommand(''))
        CheckBox4.place(width=92, height=21, x=10, y=194)
        
        button5 = ttk.Button(parent, text='Browse', command=lambda: GetDirectoryString('versionfile'))
        button5.place(width=76, height=25, x=112, y=194)

        entry2 = ttk.Entry(parent)
        entry2.place(width=248, height=21, x=198, y=197)

        button6 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('versionfile'))
        button6.place(width=40, height=25, x=456, y=194)

        label2 = tk.Label(parent, text='Script', bg=COLOR)
        label2.place(width=36, height=21, x=10, y=229)
        button7 = ttk.Button(parent, text='Browse', command=lambda: GetDirectoryString('script'))
        button7.place(width=76, height=25, x=56, y=229)
        entry3 = ttk.Entry(parent)
        entry3.place(width=354, height=21, x=142, y=229)

        self.CheckBoxVar5 = tk.StringVar()
        self.CheckBoxVar5.set('')
        CheckBox5 = ttk.Checkbutton(parent, text='--icon', variable=self.CheckBoxVar5, onvalue=' --icon',
                                    offvalue='', command=lambda: BuildCommand(''))
        CheckBox5.place(width=56, height=21, x=10, y=264)
        button8 = ttk.Button(parent, text='Browse', command=lambda: GetDirectoryString('icon'))
        button8.place(width=76, height=25, x=76, y=264)

        entry4 = ttk.Entry(parent)
        entry4.place(width=284, height=21, x=162, y=264)

        button9 = ttk.Button(parent, text='Info', width=5, command=lambda: CommandInfo('icon'))
        button9.place(width=40, height=25, x=456, y=264)

        label3 = tk.Label(parent, text='Command', bg=COLOR)
        label3.place(width=63, height=21, x=10, y=299)
        entry5 = ttk.Entry(parent)
        entry5.place(width=363, height=21, x=83, y=299)
        BuildCommand('')
        
        button10 = ttk.Button(parent, text='Build', command=RunBuild)
        button10.place(width=76, height=25, x=(506/2)-86, y=340)
        button11 = ttk.Button(parent, text='Close', command=parent.destroy)
        button11.place(width=76, height=25, x=(506/2)+10, y=340)

        ttk.Style().configure('TCheckbutton', background=COLOR)

class SetVersionFile(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        
        self.transient(parent)
        self.result = None
        self.grab_set()
        w = 506
        h = 300
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.geometry('{0}x{1}+{2}+{3}'.format(w, h, int(x), int(y)))
        self.resizable(width=False, height=False)
        self.configure(background=COLOR)
        self.title('Set Version File')
        self.wm_iconbitmap('images/python.ico')

        def GetDirectoryString(string):
            if string == 'fileversion':
                filename = filedialog.askopenfilename(filetypes=[('Version File', '*.txt')])
                entry1.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry1.insert(tk.END, str(filename))
            elif string == 'executable':
                filename = filedialog.askopenfilename(filetypes=[('Executable', '*.exe')])
                entry2.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry2.insert(tk.END, str(filename))

            entry3.delete(0, tk.END)
            string = 'pyi-set_version'
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
        label1 = tk.Label(self, image=self.logoImage)
        label1.pack(side=tk.TOP)

        def SetVersion():
            os.system('pyi-set_version "'+str(entry1.get().strip())+'" "'+str(entry2.get().strip())+'"')
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)
            entry3.insert(tk.END, 'pyi-set_version')

        label2 = tk.Label(self, text='File Version', bg=COLOR)
        label2.place(x=10, y=120)
        button1 = ttk.Button(self, text='Browse', command=lambda: GetDirectoryString('fileversion'))
        button1.place(x=80, y=120)
        entry1 = ttk.Entry(self)
        entry1.place(width=506-76-100, height=21, x=165, y=122)

        label3 = tk.Label(self, text='Executable', bg=COLOR)
        label3.place(x=10, y=155)
        button2 = ttk.Button(self, text='Browse', command=lambda: GetDirectoryString('executable'))
        button2.place(x=80, y=155)
        entry2 = ttk.Entry(self)
        entry2.place(width=330, height=21, x=165, y=157)

        label4 = tk.Label(self, text='Command', bg=COLOR)
        label4.place(x=10, y=192)
        entry3 = ttk.Entry(self)
        entry3.place(width=365, height=21, x=80, y=192)
        entry3.insert(tk.END, 'pyi-set_version')

        button4 = ttk.Button(self, text='Set Version', command=SetVersion)
        button4.place(width=76, height=25, x=(506/2)-86, y=235)
        button5 = ttk.Button(self, text='Close', command=self.destroy)
        button5.place(width=76, height=25, x=(506/2)+10, y=235)


class GrabVersionFile(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        
        self.transient(parent)
        self.result = None
        self.grab_set()
        w = 506
        h = 230
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.geometry('{0}x{1}+{2}+{3}'.format(w, h, int(x), int(y)))
        self.resizable(width=False, height=False)
        self.configure(background=COLOR)
        self.title('Set Version File')
        self.wm_iconbitmap('images/python.ico')

        def GetDirectoryString(string):
            if string == 'executable':
                filename = filedialog.askopenfilename(filetypes=[('Executable', '*.exe')])
                entry1.delete(0, tk.END)
                if filename == '':
                    pass
                else:
                    entry1.insert(tk.END, str(filename))

            entry2.delete(0, tk.END)
            string = 'pyi-grab_version'
            if str(entry1.get().strip()) == '':
                pass
            else:
                string += ' "'+str(entry1.get())+'"'
            entry2.insert(tk.END, string)

        self.logoImage = ImageTk.PhotoImage(Image.open('images/logo.png'))
        label1 = tk.Label(self, image=self.logoImage)
        label1.pack(side=tk.TOP)

        def grab_version():
            string = 'pyi-grab_version "'+str(entry1.get().strip())+'"'
            os.system(string)
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry2.insert(tk.END, 'pyi-grab_version')

        label2 = tk.Label(self, text='Executable', bg=COLOR)
        label2.place(x=10, y=120)
        button1 = ttk.Button(self, text='Browse', command=lambda: GetDirectoryString('executable'))
        button1.place(x=80, y=120)
        entry1 = ttk.Entry(self)
        entry1.place(width=506-76-100, height=21, x=165, y=122)

        label3 = tk.Label(self, text='Command', bg=COLOR)
        label3.place(x=10, y=155)
        entry2 = ttk.Entry(self)
        entry2.place(width=365, height=21, x=80, y=155)
        entry2.insert(tk.END, 'pyi-grab_version')

        button3 = ttk.Button(self, text='Grab Version', command=grab_version)
        button3.place(width=76, height=25, x=(506/2)-86, y=190)
        button4 = ttk.Button(self, text='Close', command=self.destroy)
        button4.place(width=76, height=25, x=(506/2)+10, y=190)


def main():
    root = tk.Tk()
    root.geometry('506x400')
    root.resizable(False, False)
    root.title('PyInstaller GUI Version: '+str(__version__))
    root.wm_iconbitmap('images/python.ico')
    root.configure(background=COLOR)
    MainApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
