
import sys
from tkinter import *
from functools import partial
from tkinter import ttk
import pytube.exceptions
from pytube import YouTube

class links:
    lst = []
    def add(self, link):
        print("Start Adding")
        if "https://www.youtube.com/" in link.get()[:24]:
            print(link.get())
            if link.get() not in self.lst:
                try:
                    self.lst.append(link.get())
                except AttributeError:
                    self.lst = [link.get()]
            print("End Adding\n")
            a = ttk.Label(mainframe, text=str(self.lst)).grid(column=2, row=2, sticky=(S, W))
        else:
            print("Wrong Format Adding\n")

    # Func
    def download(self):
        print("Start Downloading")
        if self.lst != []:
            print(self.lst)
        else:
            print("Empty list")
            print("Wrong Format Downloading\n")
            return
        print("")
        for i in self.lst:
            print(f"Start Downloading {self.lst.index(i) + 1}")
            print(i)
            try:
                video = YouTube(i)
                stream = video.streams.get_highest_resolution()
                stream.download()
                print(f"End Downloading {self.lst.index(i) + 1}\n")
            except pytube.exceptions.RegexMatchError:
                print(f"Error Downloading. {i} was not found\n")
        print("End Downloading\n")

    def clear(self):
        self.lst = []

# Start
# Main Application Window
root = Tk()
root.title("Download the video by link")

# Content Frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Widgets
ttk.Label(mainframe, text="Enter link:").grid(column=1, row=1)

# Entry Widget
link = StringVar()
link_entry = ttk.Entry(mainframe, width=90, textvariable=link)
link_entry.grid(column=2, row=1, sticky=(S, W))

add = partial(links.add, links, link)
ttk.Button(mainframe, text="Create", command=add).grid(column=0, row=1, sticky=(S, W))
ttk.Label(mainframe, text="List of links:").grid(column=1, row=2)

download = partial(links.download, links)
ttk.Button(mainframe, text="Download!", command=download).grid(column=0, row=2, sticky=(S, W))
clear = partial(links.clear, links)
ttk.Button(mainframe, text="Clear!", command=clear).grid(column=0, row=3, sticky=(S, W))

# Some Polish
for child in root.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Event Loop
root.mainloop()

"""
link_entry.focus()
"""