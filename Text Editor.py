import os
from tkinter import *
import tkinter.filedialog


def saveas():
    global text
    t = text.get("1.0", "end-1c")
    savelocation = tkinter.filedialog.asksaveasfilename()
    if savelocation:
        with open(savelocation, "w+") as file1:
            file1.write(t)


def auto_close(event):
    close_char = {'(': ')', '{': '}', '[': ']', '"': '"', "'": "'"}
    char = event.char
    if char in close_char:
        text.insert(INSERT, close_char[char])
        text.mark_set(INSERT, "{}-1c".format(INSERT))


root = Tk()
root.title("Text Editor")
text = Text(root)
text.grid()

text.bind("<KeyRelease>", auto_close)

button = Button(root, text="Save", command=saveas)
button.grid()

root.mainloop()
