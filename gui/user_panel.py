

from tkinter import * 
import tkinter as tk   
# from tkinter import Tk, Label, X, Frame, Y, LEFT, BOTH

from tkinter import ttk
from functools import partial

class User_Panel(Frame):

    def __init__(self, parent, tabControl,db):
        super().__init__(parent)
        self.db=db


        self.user_tab = ttk.Frame(tabControl)
        tabControl.add(self.user_tab, text ='Survey Form')

        # ttk.Label(self.user_tab, text="Survey Form", font=('Lucida 15')).grid(column = 0, row = 0, padx = 30, pady = 30)
        
        # self.user_tab.pack(side='top', fill='both', expand='True')
   

        # Initialize frames
        f1 = Frame(self.user_tab, bg="grey")
        f2 = Frame(self.user_tab, bg="pink")

        # Initialize labels
        w1 = Label(f1, text="Red", bg="red", fg="white")
        # w2 = Label(f1, text="Green", bg="green", fg="white")
        # w3 = Label(f1, text="Blue", bg="blue", fg="white")
        w1b = Label(f2, text="Red", bg="red", fg="white")
        w2b = Label(f2, text="Green", bg="green", fg="white")
        w3b = Label(f2, text="Blue", bg="blue", fg="white")

        # Packing level 1
        f1.pack(fill=BOTH)
        f2.pack(fill=BOTH, expand=True)

        # Packing level 2
        w1.pack(fill=X)
        # w2.pack(fill=X)
        # w3.pack(fill=X)
        w1b.pack(side=LEFT, fill=BOTH, expand=True)
        w2b.pack(side=LEFT, fill=BOTH, expand=True)
        w3b.pack(side=LEFT, fill=BOTH, expand=True)

