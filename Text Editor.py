import os
from tkinter import *
from tkinter import filedialog, messagebox
import keyword


class TextEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.filename = None

        self.text = Text(self.root, wrap='word', undo=True)
        self.text.grid(sticky=N+E+S+W)

        self.text.bind("<KeyRelease>", self.auto_close)
        self.text.bind("<KeyRelease>", self.syntax_highlighting, add="+")

        self.create_menu()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Undo", command=self.text.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text.edit_redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

    def new_file(self):
        self.filename = None
        self.text.delete(1.0, END)

    def open_file(self):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files",
                                              "*.txt"), ("Python Files", "*.py")]
        )
        if self.filename:
            with open(self.filename, "r") as file:
                self.text.delete(1.0, END)
                self.text.insert(END, file.read())

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.text.get(1.0, END))
        else:
            self.save_as_file()

    def save_as_file(self):
        self.filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files",
                                              "*.txt"), ("Python Files", "*.py")]
        )
        if self.filename:
            self.save_file()

    def auto_close(self, event):
        close_char = {'(': ')', '{': '}', '[': ']', '"': '"', "'": "'"}
        char = event.char
        if char in close_char:
            self.text.insert(INSERT, close_char[char])
            self.text.mark_set(INSERT, "{}-1c".format(INSERT))

    def syntax_highlighting(self, event=None):
        keywords = keyword.kwlist
        text_content = self.text.get("1.0", "end-1c")

        for kw in keywords:
            start = "1.0"
            while True:
                start = self.text.search(r'\b{}\b'.format(
                    kw), start, stopindex="end", regexp=True)
                if not start:
                    break
                end = self.text.index(f"{start}+{len(kw)}c")
                self.text.tag_add(kw, start, end)
                self.text.tag_config(kw, foreground="blue")
                start = end

        # Highlight strings
        start = "1.0"
        while True:
            start = self.text.search(
                r'\".*?\"', start, stopindex="end", regexp=True)
            if not start:
                break
            str_len = len(self.text.get(start, "end").split('"')[1]) + 2
            end = self.text.index(f"{start}+{str_len}c")
            self.text.tag_add("string", start, end)
            self.text.tag_config("string", foreground="green")
            start = end

        # Highlight comments
        start = "1.0"
        while True:
            start = self.text.search(
                r'#.*', start, stopindex="end", regexp=True)
            if not start:
                break
            end = self.text.index(f"{start} lineend")
            self.text.tag_add("comment", start, end)
            self.text.tag_config("comment", foreground="red")
            start = end


if __name__ == "__main__":
    root = Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = TextEditor(root)
    root.mainloop()
