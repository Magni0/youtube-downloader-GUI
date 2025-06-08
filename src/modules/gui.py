"""Handles the GUI fields/layout."""

import pathlib

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class GUI:

    PADY = 10
    PADX = 10

    def __init__(self, window):
        self.window = window

    def make_new_entry(self, row: int, column: int, read_only=False) -> tk.StringVar:
        text_var = tk.StringVar()
        text_var.set("")

        tk.Entry(
            self.window,
            fg="black",
            textvariable=text_var,
            disabledforeground="gray",
            bg="lightgray",
            state="readonly" if read_only else "normal",
            bd=3,
        ).grid(row=row, column=column)

        return text_var

    def make_new_listbox(self, row: int, column: int, options: list) -> tk.Listbox:
        listbox = ttk.Combobox(
            self.window,
            values=options,

        )
        
        listbox.set(options[0])

        listbox.grid(
            row=row,
            column=column
        )
        
        return listbox

    def make_new_button(self, button_text: str, method, row: int, column: int) -> tk.Button:
        """https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/"""
        button = tk.Button(
            self.window,
            command=method,
            text=button_text,
            overrelief="raised",
            default="active",
            fg="black",
            pady=5,
            padx=5,
            disabledforeground="gray",
            bg="lightgray",
            bd=3,
            activebackground="blue", 
            activeforeground="white",
        ).grid(row=row, column=column)

        return button

    def make_new_label(self, row: int, column: int, text_var=None, border=False) -> tk.StringVar:
        """https://www.geeksforgeeks.org/python-tkinter-label/"""

        if not text_var:
            text_var = tk.StringVar()
            text_var.set("")

        if border:
            label: tk.Label = tk.Label(
                self.window,
                textvariable=text_var,
                cursor="hand2",
                pady=5,
                padx=5,
                border=1,
                fg="black",
                justify=tk.CENTER,
                underline=0,
                wraplength=250
            )
        else:
            label: tk.Label = tk.Label(
                self.window,
                textvariable=text_var,
                cursor="hand2",
                fg="black",
                pady=5,
                padx=5,
                justify=tk.CENTER,
                underline=0,
                wraplength=250
            )

        label.grid(row=row, column=column)

        return text_var

    def make_new_radio_button(self, default, value_dict: dict, row: int, column: int, vertical=False, expand=True) -> tk.StringVar:
        """https://www.geeksforgeeks.org/radiobutton-in-tkinter-python/"""
        var = tk.Variable(self.window, default)

        for (text, value) in value_dict.items():
            tk.Radiobutton(
                self.window, 
                text=text, 
                variable=var, 
                value=value,
                indicator=0,
                bg="lightgray",
                fg="black",
                pady=5,
                padx=5,
                bd=3,
                activebackground="lightblue", 
                activeforeground="black",
            ).grid(
                row=row,
                column=column,
                rowspan=1,
                sticky=tk.W
            )

            if not expand:
                continue

            if vertical:
                row += 1
            else:
                column += 1
        
        return var

    def make_file_explorer_button(self, button_text: str, label_var: tk.StringVar, row: int, column: int) -> tk.Button:
        """
        https://pythonspot.com/tk-file-dialogs/
        https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
        """

        def browse_dir():
            browse_dir = filedialog.askdirectory(
                initialdir=pathlib.Path.home(),
                title=button_text,
            )
            label_var.set(browse_dir)

        return self.make_new_button(button_text=button_text, method=browse_dir, row=row, column=column)
