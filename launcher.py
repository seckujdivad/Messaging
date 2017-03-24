global flags, theme_name_entry
import tkinter as tk
import os, threading

#####

file = open('flags.py', 'r')
flags = eval(file.read())
file.close()

#####

root = tk.Tk()
root.title('Messaging Launcher')

def launch():
    flags['theme'] = theme_name_entry.get()
    file = open('flags.py', 'w')
    file.write(str(flags))
    file.close()
    os.startfile('client.vbs')

#####

go_button = tk.Button(root, text='Launch', command=launch, font=('', 15))

input_frame = tk.Frame(root)

label_frame = tk.Frame(input_frame)
theme_name_label = tk.Label(label_frame, text='Theme')

entry_frame = tk.Frame(input_frame)
theme_name_entry = tk.Entry(entry_frame)
theme_name_entry.insert(0, flags['theme'])

#####

label_frame.pack(side=tk.LEFT)
entry_frame.pack(side=tk.LEFT)

theme_name_label.pack(anchor='nw')
theme_name_entry.pack(anchor='nw')

input_frame.pack(side=tk.TOP, fill=tk.BOTH)

go_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#####

root.mainloop()
