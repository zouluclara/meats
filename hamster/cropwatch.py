#!/usr/bin/env python

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import os

def play(url_entry):
    print(url_entry.get())
    urls = os.popen('youtube-dl -g '+url_entry.get()).readlines()
    print(urls)
    if len(urls) == 1:
        os.system('mplayer -vf crop=900:500:0:220 "{}"'.format(urls[0].strip()))
    else:
        os.system('mplayer -vf crop=900:500:0:220 "{}" -audiofile "{}"'.format(*[u.strip() for u in urls]))


def show_menu(e):
    """A variation on: http://stackoverflow.com/a/8476726/1338797."""
    the_menu = tk.Menu(root, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)


root = tk.Tk()
root.title("Crop watch URL")
#root.geometry("600x50")

url = tk.Entry(root, width=80)
url.bind('<Button-3><ButtonRelease-3>', show_menu)
url.pack(anchor=tk.N)

watch = tk.Button(root, text='Watch', command=lambda: play(url), width=80)
watch.pack(anchor=tk.N)

root.mainloop()

