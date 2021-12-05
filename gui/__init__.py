
import tkinter as tk                    
from tkinter import ttk
from tkinter.constants import *

from database import Database
from .admin_panel import Admin_Panel
from .user_panel import User_Panel


class GUI(tk.Tk):



    BKGR_IMAGE_PATH = 'gui/img/survey_bg.png'


    def __init__(self,database_filename, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
        self.db = Database(database_filename)
        # self.minsize(1080, 720)    
        self.geometry("1080x720")


        self.title("Singing Sculpture Survey")



        



        self.state('zoomed')
        # self.attributes('-fullscreen',True)


        self.tabControl = ttk.Notebook(self)


   
        User_Panel(self, self.tabControl,self.db)  
        Admin_Panel(self, self.tabControl,self.db)


        self.tabControl.pack(expand=True, fill ="both")


        # self.bkgr_image = tk.PhotoImage(file=self.BKGR_IMAGE_PATH)



    def run_mainloop(self):
        self.lift()
        self.attributes('-topmost', True)
        self.mainloop() 


