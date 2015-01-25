#!usr/bin/env/python
from os import walk, remove
from os.path import normpath, join
from tkinter import *
from tkinter.filedialog import askdirectory
from shutil import copy2, rmtree, move, Error as ShutilError


def flatten(origin, destination, in_place, rmv_empty_dirs=False):
    """Flattens the origin directory into the destination directory or itself"""
    origin = normpath(origin)
    destination = normpath(destination)
    for root, dirs, files in walk(origin):
        for file in files:
            if in_place:
                try:
                    move(join(root, file), origin)
                except ShutilError:
                    if root != origin:
                        remove(join(root, file))
            else:
                copy2(join(root, file), destination)
    if rmv_empty_dirs:
        root, dirs, files = next(walk(origin))
        for directory in dirs:
            rmtree(origin + '\\' + directory)


def get_path(txt):
    """Fills the given Entry field with the selected path from Explorer"""
    txt.delete(0, END)
    txt.insert(0, askdirectory())
    return


def destination_status(disable):
    """Disable entry field"""
    new_state = "disabled" if disable else "normal"
    txt_destination.configure(state=new_state)
    txt_destination.update()


def rmv_empty_dirs(disable):
    """Disable check box"""
    new_state = "disabled" if disable else "normal"
    cbx_rmv_dirs.configure(state=new_state)
    cbx_rmv_dirs.update()


def combine_funcs(*funcs):
    """Combine functions to be passed to a button"""

    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


# Window setup
window = Tk()
window.title('Flatten Directory')
window.geometry('+300+200')
window.resizable(0, 0)

btnheight = 1
btnwidth = 3

# Origin file
lbl_origin = Label(window, text='Origin:').grid(row=0, sticky=E)
txt_origin = Entry(window, width=45)
txt_origin.grid(row=0, column=1, columnspan=2, padx=(0, 10))
btn_origin = Button(text='...',
                    command=lambda: get_path(txt_origin),
                    height=btnheight,
                    width=btnwidth)
btn_origin.grid(row=0, column=3, pady=(5, 10), sticky=W)

# Destination file
lbl_destination = Label(window, text='Destination:').grid(row=1, sticky=E)
txt_destination = Entry(window, width=45)
txt_destination.grid(row=1, column=1, columnspan=2, padx=(0, 10))
btn_destination = Button(text='...',
                         command=lambda: get_path(txt_destination),
                         height=btnheight,
                         width=btnwidth)
btn_destination.grid(row=1, column=3, pady=(5, 10), sticky=W)

# Copy to destination or flatten in-place
choice = IntVar()
choice.set(0)

rdo_copy = Radiobutton(window,
                       text='Copy to destination',
                       command=lambda:
                       combine_funcs(
                           destination_status(choice.get()),
                           rmv_empty_dirs(abs(choice.get()-1)),
                           rmv_dirs.set(0)),
                       variable=choice,
                       val=0)
rdo_copy.grid(row=2, column=1, padx=(0, 5), sticky=W)

rdo_inplace = Radiobutton(window,
                          text='Flatten in place',
                          command=lambda: combine_funcs(
                              destination_status(choice.get()),
                              rmv_empty_dirs(abs(choice.get()-1))),
                          variable=choice,
                          val=1)
rdo_inplace.grid(row=2, column=2, sticky=W)

# Check whether or not to remove empty directories after flattening in place
rmv_dirs = IntVar()
rmv_dirs.set(0)

cbx_rmv_dirs = Checkbutton(window,
                           text='Remove empty directories',
                           justify=LEFT,
                           variable=rmv_dirs)
cbx_rmv_dirs.grid(row=3, column=2, sticky=W)
cbx_rmv_dirs.configure(state="disabled")

# Flatten origin into destination
btn_flatten = Button(text='Accept',
                     command=lambda: flatten(txt_origin.get(),
                                             txt_destination.get(),
                                             choice.get(),
                                             rmv_dirs.get()))
btn_flatten.grid(row=2, column=3, padx=(0, 5), pady=5, sticky=W)

window.mainloop()
