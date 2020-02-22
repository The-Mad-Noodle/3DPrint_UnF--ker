'''
-----------------------------------------------------------------------------------------
   _____ ____     ____       _       __     __  __      ______           __
  |__  // __ \   / __ \_____(_)___  / /_   / / / /___  / ____/_  _______/ /_____  _____
   /_ </ / / /  / /_/ / ___/ / __ \/ __/  / / / / __ \/ /_  / / / / ___/ //_/ _ \/ ___/
 ___/ / /_/ /  / ____/ /  / / / / / /_   / /_/ / / / / __/ / /_/ / /__/ ,< /  __/ /
/____/_____/  /_/   /_/  /_/_/ /_/\__/   \____/_/ /_/_/    \__,_/\___/_/|_|\___/_/
                                                        by The Mad Noodle v.0.0.6
-----------------------------------------------------------------------------------------
The Failed 3D print recovery gcode processor.
Find the line number of the point where your 3D print failed
and the UnF**ker will modify the gcode to start at the correct point

By The Mad Noodle
02/05/2020
v0.0.6
'''

# TODO Create SFW version of the software (3D PUF)

import os
import subprocess
import platform
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox as mb
import configparser
import webbrowser

# == Configuration Setup ==============================================================

# TODO Create configuration window.
#  -Option to save and load different printer config files
#  -with save button and load print "drop down"
#  -Separate config files to new folder

configFile = 'config.ini'
config = configparser.ConfigParser()
config.read(configFile)

# TODO Add firmware options, I.E. Marlin, Smoothie, Makerbot
start_z_move = config.get('settings', 'start_z_move')
recovered_suffix = config.get('settings', 'recovered_file_suffix')
default_open_dir = config.get('settings', 'default_open_dir')

github_URL = 'https://github.com/The-Mad-Noodle/'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is Project Root
EXAMPLE_PATH = os.path.join(ROOT_DIR, 'example')


# == Functions ========================================================================

def main_window():
    open_example_folder = lambda: open_file(EXAMPLE_PATH)
    open_github_main = lambda: webbrowser.open_new_tab(github_URL)
    open_github_3DPF = lambda: webbrowser.open_new_tab(github_URL + '3DPrint-UnF**ker')
    open_TMN_website = lambda: webbrowser.open_new_tab('https://www.instagram.com/the_mad_noodle/')

    def fix_gcode():
        try:
            recovery_filename = source_text.get()
            line_number = int(line_field.get())
            Z_height = float(z_field.get())
            print_temp = temp_field.get()

            Z_height_offset = float(Z_height) + float(start_z_move)

            if recovery_filename[-6:] != '.gcode':
                mb.showerror("Wrong File Format", "Incorrect file format!\n"
                                                  "Please select a .gcode file and try again.")
                recovery_filename = ''
                source_text.delete(0, END)
                source_text.insert(0, '')

            i = 0
            x = 0
            # TODO Add option to save Recovery to a different destination
            f = open(recovery_filename, "r")
            destination_name = recovery_filename[:-6]
            destination_file = destination_name + '_' + recovered_suffix + '.gcode'
            copy = open(destination_file, "wt")

            line = f.readline()

            for line in f:
                if x == (line_number - 2):
                    try:
                        last_E = line.split('E', 1)[1]
                    except:
                        mb.showerror("error", "This is not a usable line number!\n"
                                              "Add or subtract a few from your current number and try again.")
                x = x + 1

            # TODO Create additional scripts for other firmwares
            inserted_gcode = ["; " + recovery_filename + " failed at line " + str(line_number) + "\n",
                              "; gCode Defuct with Print Unf**ker v.0.0.6 by The Mad Noodle\n\n"
                              "G90\n", "M82\n", "G28 X0 Y0\n\n", "M201 X500 Y500; Set X and Y acceleration values\n",
                              "M204 S500; Set default acceleration\n\n",
                              "M104 S" + str(print_temp) + " T0\n", "M109 S" + str(print_temp) + " T0\n\n",
                              "M117 God Speed and Good Luck\n\n",
                              "T0\n", "G92 E" + str(last_E) + "\n", "G92 Z" + str(Z_height_offset) + "\n\n\n", ]

            copy.writelines(inserted_gcode)
            f.seek(0)

            for line in f:
                if i >= (line_number - 2):
                    copy.write(str(line))

                if i == (line_number) - 2:
                    copy.write("G1 Z" + str(Z_height) + "\n")

                i = i + 1
            f.close()
            copy.close()

            # TODO Open containing folder rather than the file
            if mb.askyesno('Done', 'Your print is now UnF**ked!\nWould you like to review your gcode?'):
                open_file(destination_file)

            else:
                print('done')
        except:
            mb.showerror("error", "This is not a usable line number!\n"
                                  "Add or subtract a few from your current number and try again.")

    def open_source_file():
        global recovery_filename
        window.source_filename = filedialog.askopenfilename(initialdir=default_open_dir, title="Select Source file",
                                                            filetypes=(
                                                                ("gCode files", "*.gcode"), ("all files", "*.*")))
        source_text.delete(0, END)
        source_text.insert(0, '')
        source_text.insert(END, window.source_filename)

    def open_file(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def hello():
        print('Hello')

    # == GUI Setup ==================================================================

    # TODO Add menu bar at the top of window (File and Help)
    #  -Link Github and instructional texts in help menu
    #  -Add File menu house the configuration option
    window = Tk()

    window.title("3D Print UnF**ker v.0.0.6")
    # window.geometry('270x100')
    window.iconbitmap('img/unf_SFW.ico')
    menubar = Menu(window)

    s = Style()
    s.configure('My.TFrame', relief=RAISED)

    # -- Menu Bar for main window
    # File
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Config Edit", command=config_window)
    filemenu.add_command(label="Open", command=hello)
    filemenu.add_command(label="Save", command=hello)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    # Edit
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cut", command=hello)
    editmenu.add_command(label="Copy", command=hello)
    editmenu.add_command(label="Paste", command=hello)
    menubar.add_cascade(label="Edit", menu=editmenu)
    # Help
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=open_github_3DPF)
    helpmenu.add_command(label="Github", command=open_github_main)
    helpmenu.add_command(label="Website", command=open_TMN_website)
    helpmenu.add_command(label="Example", command=open_example_folder)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    window.config(menu=menubar)

    main_frame = Frame(window)
    main_frame.pack()

    # -- Logo
    logo_img = PhotoImage(file='img/logo_sfw.png')
    title_lbl = Label(main_frame, image=logo_img, font='courier')
    title_lbl.grid(columnspan=3, row=0, padx=5, pady=5)

    # -- Source file select
    source_btn = Button(main_frame, text="Open Gcode", command=open_source_file)
    source_btn.grid(column=0, row=1, padx=5, pady=5)
    source_text = Entry(main_frame)
    source_text.grid(column=1, row=1, padx=5, pady=5)

    # -- Line number field
    line_lbl = Label(main_frame, text='Line Number:')
    line_lbl.grid(column=0, row=2, sticky=E, padx=5, pady=5)
    line_field = Entry(main_frame)
    line_field.grid(column=1, row=2, sticky=W, padx=5, pady=5)

    # -- Z height field
    z_lbl = Label(main_frame, text='Z-Height:')
    z_lbl.grid(column=0, row=3, sticky=E, padx=5, pady=5)
    z_field = Entry(main_frame)
    z_field.grid(column=1, row=3, sticky=W, padx=5, pady=5)

    # -- temp field
    temp_lbl = Label(main_frame, text='Temperature:')
    temp_lbl.grid(column=0, row=4, sticky=E, padx=5, pady=5)
    temp_field = Entry(main_frame)
    temp_field.grid(column=1, row=4, sticky=W, padx=5, pady=5)

    # -- UnF**k Button
    button_img = PhotoImage(file='img/button_label_sfw.png')
    unfuck_btn = Button(main_frame, image=button_img, command=fix_gcode)
    unfuck_btn.grid(column=1, columnspan=2, row=5, sticky=E, padx=5, pady=5)

    window.mainloop()


def config_window():

    def save_config():
        config['settings']['start_z_move'] = start_z_field.get()
        config['settings']['recovered_file_suffix'] = recovered_suffix_field.get()
        config['settings']['default_open_dir'] = default_open_dir_field.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        if mb.askyesno('Done', 'Your configs are saved!\nA refresh is required before your new settings can take effect.\nWould you like to refesh now?'):
            os.execl(sys.executable, sys.executable, *sys.argv)

    config_win = Tk()
    config_win.title('3DPUF Config')
    config_win.iconbitmap('img/unf_SFW.ico')

    config_title_lbl = Label(config_win, text='Configuration', font='courier')
    config_title_lbl.grid(columnspan=2, row=0, padx=5, pady=5)

    # -- Line number field
    start_z_lbl = Label(config_win, text='Start Z Lift Height:')
    start_z_lbl.grid(column=0, row=2, sticky=E, padx=5, pady=5)
    start_z_field = Entry(config_win)
    start_z_field.grid(column=1, row=2, sticky=W, padx=5, pady=5)
    start_z_field.insert(END, start_z_move)

    recovered_suffix_lbl = Label(config_win, text='Recovery File Suffix:')
    recovered_suffix_lbl.grid(column=0, row=3, sticky=E, padx=5, pady=5)
    recovered_suffix_field = Entry(config_win)
    recovered_suffix_field.grid(column=1, row=3, sticky=W, padx=5, pady=5)
    recovered_suffix_field.insert(END, recovered_suffix)

    default_open_dir_lbl = Label(config_win, text='Default Open Directory:')
    default_open_dir_lbl.grid(column=0, row=4, sticky=E, padx=5, pady=5)
    default_open_dir_field = Entry(config_win)
    default_open_dir_field.grid(column=1, row=4, sticky=W, padx=5, pady=5)
    default_open_dir_field.insert(END, default_open_dir)

    config_save_btn = Button(config_win, text='Save Configs', command=save_config)
    config_save_btn.grid(columnspan=2, row=5, padx=5, pady=5)

    config_win.mainloop()




if __name__ == '__main__':
    main_window()
