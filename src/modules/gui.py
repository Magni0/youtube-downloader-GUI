"""Handles the GUI fields/layout."""

import pathlib

import tkinter as tk
from tkinter import filedialog

class GUI:

    PADY = 10
    PADX = 10

    def __init__(self, window):
        self.window = window

    def make_new_entry(self, row: int, column: int):
        text_var = tk.StringVar()
        text_var.set("")

        tk.Entry(
            self.window,
            overrelief="raised",
            fg="black",
            disabledforeground="gray",
            bg="lightgray",
            bd=3,
        ).grid(row=row, column=column)

        return text_var

    def make_new_button(self, button_text: str, method, row: int, column: int) -> tk.Button:
        """https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/"""
        button = tk.Button(
            self.window,
            command=method,
            text=button_text,
            overrelief="raised",
            fg="black",
            disabledforeground="gray",
            bg="lightgray",
            bd=3,
            activebackground="blue", 
            activeforeground="white",
        ).grid(row=row, column=column)

        return button

    def make_new_label(self, row: int, column: int, text_var=None) -> tk.StringVar:
        """https://www.geeksforgeeks.org/python-tkinter-label/"""

        if not text_var:
            text_var = tk.StringVar()
            text_var.set("")

        label = tk.Label(
            self.window,
            textvariable=text_var,
            height=3,
            width=30,
            cursor="hand2",
            fg="red",
            justify=tk.CENTER,
            relief=tk.RAISED,
            underline=0,
            wraplength=250
        )

        label.grid(row=row, column=column)

        return text_var

    def make_new_radio_button(self, var_text: str, value_dict: dict, row: int, column: int, vertical=False, button=True) -> tk.StringVar:
        """https://www.geeksforgeeks.org/radiobutton-in-tkinter-python/"""
        var = tk.Variable(self.window, var_text)

        for (text, value) in value_dict.items():
            radio_button = tk.Radiobutton(
                self.window, 
                text=text, 
                variable=var, 
                value=value, 
                indicator=0,
                bg="lightgray",
                fg="black",
                bd=3,
                activebackground="lightblue", 
                activeforeground="black",
            )

            if button:
                radio_button.grid(
                    fill=tk.X,
                    row=row,
                    column=column
                )
            else:
                radio_button.grid(
                    side=tk.TOP,
                    row=row,
                    column=column
                )
            
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
