import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename

def create_button(grid_frame, row, column, text, command, columnspan=1, padx=5, pady=5, sticky=tk.N+tk.E+tk.S+tk.W):
    button = tk.Button(grid_frame, text=text, command = command)
    button.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
    return button

def create_label(grid_frame, row, column, text='', columnspan=1, padx=5, pady=5):
    label = tk.Label(grid_frame, text=text)
    label.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return label

def create_slider(grid_frame, row, column, min, max, start_value=max, columnspan=1, orient='horizontal', padx=5, pady=5, sticky=tk.N+tk.E+tk.S+tk.W):
    slider = tk.Scale(grid_frame, from_=min, to=max, orient=orient)
    slider.set(start_value)
    slider.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
    return slider