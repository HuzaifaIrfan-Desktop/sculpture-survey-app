

#################################################################################
####################  Admin Panel Classes #######################################
#################################################################################


from tkinter import *
from tkinter import filedialog

import tkinter as tk
from tkinter import ttk
from functools import partial
import os
from .survey_format import survey_format
import csv

from pathlib import Path
import os

# ASSETS_PATH = Path(__file__).resolve().parent / "assets"


ASSETS_PATH = os.path.abspath(os.path.join(os.pardir,'assets'))

###########################
# Admin Panel Frames Controller
###########################


class Admin_Panel(Frame):

    def __init__(self, parent, tabControl, db):
        super().__init__(parent)
        self.db = db

        self.configure(background="#3A7FF6")

        self.admin_tab = Frame(tabControl)
        tabControl.add(self.admin_tab, text='Admin Panel')

        self.admin_tab.grid_rowconfigure(0, weight=1)
        self.admin_tab.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Register_Frame, Login_Frame, Admin_Frame, Settings_Frame):
            frame = F(self.admin_tab, self, db)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        if(self.db.empty_admin_password()):
            self.show_frame(Register_Frame)
        else:
            self.show_frame(Login_Frame)
      

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


###########################
# Register Frame
###########################
class Register_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)

        self.db = db
        self.controller = controller

        self.admin_tab = parent
        self.configure(background="#3A7FF6")

        f1 = Frame(self)

        f11 = Frame(f1)

        Label(f11, text="Register", font=("Arial 30 bold")).pack(
            fill=X, expand=False, padx=20, pady=20)

        # Password Label and Password Entry Box
        Label(f11, font=('Lucida 15'), text="Password").pack()
        self.password = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.password, show='*').pack()

        Label(f11, font=('Lucida 15'), text="Retype Password").pack()
        self.retypepassword = StringVar()
        Entry(f11, font=('Lucida 15'),
              textvariable=self.retypepassword, show='*').pack()



        # Register Button
        Button(f11, font=('Lucida 15'), text="Create Admin Password",
               command=self.validateRegister).pack(padx=10, pady=10)

        self.ValidationText = StringVar(value="")
        Label(f11, font=('Lucida 10'), textvariable=self.ValidationText).pack()

        f11.place(anchor="c", relx=.5, rely=.5)

        f1.place(anchor="c", relx=.5, rely=.5, height=500, width=500)

    def validateRegister(self):
        password = self.password.get()
        retypepassword = self.retypepassword.get()

        if len(password) == 0:
            self.ValidationText.set("Password is Required")
            return False

        if len(password) <= 4:
            self.ValidationText.set(
                "Password must contain more than 4 Characters")
            return False
        else:
            if (retypepassword == password):
                self.db.set_admin_password(password)
                self.controller.show_frame(Admin_Frame)
                self.password.set('')
                self.retypepassword.set('')

                return True
            else:
                self.ValidationText.set("Password Do not Match")

        return False


###########################
# Login Frame
###########################

class Login_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db = db
        self.controller = controller

        self.configure(background="#3A7FF6")

        f1 = Frame(self)

        f11 = Frame(f1)

        Label(f11, text="Login", font=("Arial 30 bold")).pack(
            fill=X, expand=False, padx=20, pady=20)

        # Password Label and Password Entry Box
        Label(f11, font=('Lucida 15'), text="Password").pack()
        self.password = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.password, show='*').pack()

        # Login button
        Button(f11, font=('Lucida 15'), text="Login",
               command=self.validateLogin).pack(padx=10, pady=10)

        self.ValidationText = StringVar(value="")
        Label(f11, font=('Lucida 10'), textvariable=self.ValidationText).pack()
        self.ValidationText.set("")

        f11.place(anchor="c", relx=.5, rely=.5)

        f1.place(anchor="c", relx=.5, rely=.5, height=500, width=500)

    def validateLogin(self):
        password = self.password.get()

        if len(password) == 0 or password == '':
            self.ValidationText.set("Please Enter your Password")
            return False


        if(self.db.check_admin_password(password)):
            self.ValidationText.set("")
            self.password.set('')
            self.controller.show_frame(Admin_Frame)
            return True

        else:
            self.ValidationText.set("Invalid Password")
            return False


###########################
# Admin Frame
###########################

class Admin_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db = db
        self.controller = controller

        self.configure(background="#3A7FF6")

        self.admin_tab = parent
        Label(self, bg='#3A7FF6',  text="Admin Panel", font=('Lucida 15')).pack()

        self.headings = ('ID', 'Firstname', 'Lastname', 'Age', 'Gender', 'Ethnicity',
                         'Disabled', 'Enjoyed', 'Curious', 'Want to know more Science',)

        ###########################
        # Survey Table
        ###########################

        f3 = Frame(self, bg='#3A7FF6')

        Label(f3, bg='#3A7FF6', text="Surveys", font=(
            "Arial 30 bold")).pack(fill=X, expand=False)

        self.listBox = ttk.Treeview(f3, columns=self.headings, show='headings')

        for n, col in enumerate(self.headings):
            self.listBox.column(n, anchor=CENTER, stretch=NO, width=100)
            self.listBox.heading(col, text=col)
        self.listBox.column(1, anchor=CENTER, stretch=NO, width=50)
        self.listBox.column(0, anchor=CENTER, stretch=NO, width=50)
        self.listBox.column(9, anchor=CENTER, stretch=NO, width=170)
        self.listBox.pack(fill=BOTH, expand=True, padx=10, pady=10)

        f3.pack(fill=BOTH, expand=True)

        f1 = Frame(self, bg='#3A7FF6')

        f11 = Frame(f1, bg='#3A7FF6')

        ###########################
        # Average Age Frame
        ###########################

        f111 = Frame(f11, bg='#3A7FF6')
        Label(f111, text='Average Age', bg='#3A7FF6', font=('Lucida 15')).pack()
        self.AverageAgeText = StringVar(value="")
        Label(f111, textvariable=self.AverageAgeText,
              bg='#3A7FF6', font=('Lucida 12')).pack()
        f111.pack(fill=BOTH, expand=True, side=LEFT)

        ###########################
        # Gender Stats Table
        ###########################

        f112 = Frame(f11, bg='#3A7FF6')
        Label(f112, text='Gender', bg='#3A7FF6',
              font=('Lucida 15')).pack(side=TOP)
        self.gender_table = ttk.Treeview(
            f112, height=5, column=("c1", "c2", ), show='headings')

        self.gender_table.column(0, anchor=tk.CENTER)

        self.gender_table.heading(0, text="Gender")
        self.gender_table.column(0, anchor=CENTER, stretch=NO, width=100)

        self.gender_table.column(1, anchor=tk.CENTER)

        self.gender_table.heading(1, text="Count")
        self.gender_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.gender_table.pack()

        self.GenderText = {}

        self.gender_table.delete(*self.gender_table.get_children())
        for key, value in survey_format['gender']['values'].items():
            self.GenderText[key] = StringVar(value="")
            self.gender_table.insert("", "end", values=(
                value, self.GenderText[key].get(),))

        f112.pack(fill=BOTH, expand=True, side=LEFT)

        ###########################
        # Ethnicity Stats Table
        ###########################

        f113 = Frame(f11, bg='#3A7FF6')
        Label(f113, text='Ethnicity', bg='#3A7FF6',
              font=('Lucida 15')).pack(side=TOP)
        self.ethnicity_table = ttk.Treeview(
            f113, height=5, column=("c1", "c2", ), show='headings')

        self.ethnicity_table.column(0, anchor=tk.CENTER)

        self.ethnicity_table.heading(0, text="Ethnicity")
        self.ethnicity_table.column(0, anchor=CENTER, stretch=NO, width=100)

        self.ethnicity_table.column(1, anchor=tk.CENTER)

        self.ethnicity_table.heading(1, text="Count")
        self.ethnicity_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.ethnicity_table.pack()

        self.EthnicityText = {}

        self.ethnicity_table.delete(*self.ethnicity_table.get_children())
        for key, value in survey_format['ethnicity']['values'].items():
            self.EthnicityText[key] = StringVar(value="")
            self.ethnicity_table.insert("", "end", values=(
                value, self.EthnicityText[key].get(),))

        f113.pack(fill=BOTH, expand=True, side=LEFT)

        ###########################
        # Disabled Stats Table
        ###########################

        f114 = Frame(f11, bg='#3A7FF6')
        Label(f114, text='Disabled', bg='#3A7FF6',
              font=('Lucida 15')).pack(side=TOP)
        self.disabled_table = ttk.Treeview(
            f114, height=5, column=("c1", "c2", ), show='headings')

        self.disabled_table.column(0, anchor=tk.CENTER)

        self.disabled_table.heading(0, text="Disabled")
        self.disabled_table.column(0, anchor=CENTER, stretch=NO, width=100)

        self.disabled_table.column(1, anchor=tk.CENTER)

        self.disabled_table.heading(1, text="Count")
        self.disabled_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.disabled_table.pack()

        self.DisabledText = {}

        self.disabled_table.delete(*self.disabled_table.get_children())
        for key, value in survey_format['disabled']['values'].items():
            self.DisabledText[key] = StringVar(value="")
            self.disabled_table.insert("", "end", values=(
                value, self.DisabledText[key].get(),))

        f114.pack(fill=BOTH, expand=True, side=LEFT)

        ###########################
        # Enjoyed Stats Table
        ###########################

        f115 = Frame(f11, bg='#3A7FF6')
        Label(f115, text='Enjoyed', bg='#3A7FF6',
              font=('Lucida 15')).pack(side=TOP)
        self.enjoyed_table = ttk.Treeview(
            f115, height=5, column=("c1", "c2", ), show='headings')

        self.enjoyed_table.column(0, anchor=tk.CENTER)

        self.enjoyed_table.heading(0, text="Enjoyed")
        self.enjoyed_table.column(0, anchor=CENTER, stretch=NO, width=100)

        self.enjoyed_table.column(1, anchor=tk.CENTER)

        self.enjoyed_table.heading(1, text="Count")
        self.enjoyed_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.enjoyed_table.pack()

        self.EnjoyedText = {}

        self.enjoyed_table.delete(*self.enjoyed_table.get_children())
        for key, value in survey_format['enjoyed']['values'].items():
            self.EnjoyedText[key] = StringVar(value="")
            self.enjoyed_table.insert("", "end", values=(
                value, self.EnjoyedText[key].get(),))

        f115.pack(fill=BOTH, expand=True, side=LEFT)

        ###########################
        # Curious Stats Table
        ###########################

        f116 = Frame(f11, bg='#3A7FF6')
        Label(f116, text='Curious', bg='#3A7FF6',
              font=('Lucida 15')).pack(side=TOP)
        self.curious_table = ttk.Treeview(
            f116, height=5, column=("c1", "c2", ), show='headings')

        self.curious_table.column(0, anchor=tk.CENTER)

        self.curious_table.heading(0, text="Curious")
        self.curious_table.column(0, anchor=CENTER, stretch=NO, width=100)

        self.curious_table.column(1, anchor=tk.CENTER)

        self.curious_table.heading(1, text="Count")
        self.curious_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.curious_table.pack()

        self.CuriousText = {}

        self.curious_table.delete(*self.curious_table.get_children())
        for key, value in survey_format['curious']['values'].items():
            self.CuriousText[key] = StringVar(value="")
            self.curious_table.insert("", "end", values=(
                value, self.CuriousText[key].get(),))

        f116.pack(fill=BOTH, expand=True, side=LEFT)

        ###########################
        # Science Stats Table
        ###########################

        f117 = Frame(f11, bg='#3A7FF6')
        Label(f117, text='Want to know more Science',
              bg='#3A7FF6', font=('Lucida 15')).pack(side=TOP)
        self.science_table = ttk.Treeview(
            f117, height=5, column=("c1", "c2", ), show='headings')

        self.science_table.column(0, anchor=tk.CENTER)

        self.science_table.heading(0, text="Science")
        self.science_table.column(0, anchor=CENTER, stretch=NO, width=100)

        self.science_table.column(1, anchor=tk.CENTER)

        self.science_table.heading(1, text="Count")
        self.science_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.science_table.pack()

        self.ScienceText = {}

        self.science_table.delete(*self.science_table.get_children())
        for key, value in survey_format['science']['values'].items():
            self.ScienceText[key] = StringVar(value="")
            self.science_table.insert("", "end", values=(
                value, self.ScienceText[key].get(),))

        f117.pack(fill=BOTH, expand=True, side=LEFT)

        f11.pack(fill=BOTH, expand=True, padx=10, pady=10)

        ###########################
        # Refresh and Save Table
        ###########################

        f12 = Frame(f1, bg="#3A7FF6")
        Button(f12, font=('Lucida 10'), text="Refresh", width=15, command=self.refresh_data).pack(
            side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        Button(f12, font=('Lucida 10'), text="Save as CSV", width=15, command=self.ask_file_save).pack(
            side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        f12.pack(fill=Y, expand=True)

        f1.pack(fill=BOTH, expand=True)

        ###########################
        # Bottom Admin Page NavBar
        ###########################

        f2 = Frame(self, bg="pink", height=80)

        f21 = Frame(f2, bg="pink")
        Button(f21, width=20, font=('Lucida 20'), text="Settings", command=lambda: self.controller.show_frame(
            Settings_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f21.pack(side=LEFT, fill=Y, expand=True)

        f22 = Frame(f2, bg="pink")
        Button(f22, width=20, font=('Lucida 20'), text="Logout", command=lambda: self.controller.show_frame(
            Login_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f22.pack(side=LEFT, fill=Y, expand=True)

        f23 = Frame(f2, bg="pink")
        Button(f23, width=20, font=('Lucida 20'), text="Exit", command=self.exit_app).pack(
            fill=BOTH, expand=True, padx=10, pady=10)
        f23.pack(side=LEFT, fill=Y, expand=True)

        f2.pack(anchor=S, fill=X, expand=True)
        f2.pack_propagate(0)

        self.surveys = []

        self.refresh_data()

    def refresh_data(self):

        self.surveys = self.db.get_all_surveys()

        age_list = []
        for n, survey in enumerate(self.surveys):
            asurvey = list(survey)

            age_list.append(survey[3])
            asurvey[4] = survey_format['gender']['values'][survey[4]]
            asurvey[5] = survey_format['ethnicity']['values'][survey[5]]
            asurvey[6] = survey_format['disabled']['values'][survey[6]]
            asurvey[7] = survey_format['enjoyed']['values'][survey[7]]
            asurvey[8] = survey_format['curious']['values'][survey[8]]
            asurvey[9] = survey_format['science']['values'][survey[9]]
            self.surveys[n] = asurvey

        try:
            self.average_age = (sum(age_list))/len(age_list)
        except:
            self.average_age = 0

        self.AverageAgeText.set(self.average_age)

        self.gender_table.delete(*self.gender_table.get_children())
        for key, value in survey_format['gender']['values'].items():
            self.GenderText[key].set(self.db.get_gender_count(key))
            self.gender_table.insert("", "end", values=(
                value, self.GenderText[key].get(),))

        self.ethnicity_table.delete(*self.ethnicity_table.get_children())
        for key, value in survey_format['ethnicity']['values'].items():
            self.EthnicityText[key].set(self.db.get_ethnicity_count(key))
            self.ethnicity_table.insert("", "end", values=(
                value, self.EthnicityText[key].get(),))

        self.disabled_table.delete(*self.disabled_table.get_children())
        for key, value in survey_format['disabled']['values'].items():
            self.DisabledText[key].set(self.db.get_disabled_count(key))
            self.disabled_table.insert("", "end", values=(
                value, self.DisabledText[key].get(),))

        self.enjoyed_table.delete(*self.enjoyed_table.get_children())
        for key, value in survey_format['enjoyed']['values'].items():
            self.EnjoyedText[key].set(self.db.get_enjoyed_count(key))
            self.enjoyed_table.insert("", "end", values=(
                value, self.EnjoyedText[key].get(),))

        self.curious_table.delete(*self.curious_table.get_children())
        for key, value in survey_format['curious']['values'].items():
            self.CuriousText[key].set(self.db.get_curious_count(key))
            self.curious_table.insert("", "end", values=(
                value, self.CuriousText[key].get(),))

        self.science_table.delete(*self.science_table.get_children())
        for key, value in survey_format['science']['values'].items():
            self.ScienceText[key].set(self.db.get_science_count(key))
            self.science_table.insert("", "end", values=(
                value, self.ScienceText[key].get(),))

        self.listBox.delete(*self.listBox.get_children())

        for i, args in enumerate(self.surveys, start=1):
            self.listBox.insert("", "end", values=(*args,))

    def ask_file_save(self):
        data = self.surveys

        file_name = tk.filedialog.asksaveasfilename(
            initialdir="", title="Save as CSV", filetypes=(("CSV file", "*.csv"),),)
        # print (file_name)
        self.master.master.master.bring_to_front()
        if (file_name == None or file_name == ''):
            return

        if(not str(file_name).endswith(".csv")):
            file_name = str(file_name)+'.csv'

        self.save_csv(file_name, self.headings, data)
        # print('Saved Csv')

    def save_csv(self, file_name, headings, data):
        with open(file_name, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows(data)

    def exit_app(self):
        # print('Exitted')
        self.master.master.master.destroy()


###########################
# Settings Frame
###########################

class Settings_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db = db
        self.controller = controller

        self.configure(background="#3A7FF6")

        self.admin_tab = parent

        Label(self, bg="#3A7FF6", text="Admin Panel", font=('Lucida 15')).pack()

        Label(self, bg="#3A7FF6", text="Settings", font=(
            "Arial 30 bold")).pack(fill=X, expand=False)

        f1 = Frame(self)

        f11 = Frame(f1)

        Label(f11, font=('Lucida 15'), text="Password").pack()
        self.password = StringVar()
        Entry(f11, font=('Lucida 15'), textvariable=self.password, show='*').pack()

        self.ValidationText = StringVar(value="")
        Label(f11, font=('Lucida 20'), textvariable=self.ValidationText).pack()

        f111 = Frame(f11)
        Label(f111, font=('Lucida 15'), text="Change Password").pack()

        Label(f111, font=('Lucida 15'), text="New Password").pack()
        self.newpassword = StringVar()
        Entry(f111, font=('Lucida 15'),
              textvariable=self.newpassword, show='*').pack()

        Label(f111, font=('Lucida 15'), text="Retype New Password").pack()
        self.retypenewpassword = StringVar()
        Entry(f111, font=('Lucida 15'),
              textvariable=self.retypenewpassword, show='*').pack()

        Button(f111, font=('Lucida 15'), text="Change Password",
               command=self.change_password).pack()

        f111.pack(fill=BOTH, expand=True, padx=40, pady=40)

        f11.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        f12 = Frame(f1)


        f121 = Frame(f12)

        

        Label(f121, font=('Lucida 20'), fg='red', text="Danger").pack()

        Button(f121, font=('Lucida 20'), bg='red', fg='white', text="Reset Database",
               command=self.reset_database).pack(side=LEFT, padx=10, pady=10)

        Button(f121, font=('Lucida 20'), bg='red', fg='white', text="Delete Surveys",
               command=self.delete_surveys).pack(side=LEFT, padx=10, pady=10)

        f121.pack(fill=Y, expand=True, padx=10, pady=10)

        Button(f12, font=('Lucida 20'), text="Toggle Fullscreen",
               command=self.toggle_fullscreen).pack( padx=10, pady=10)

        f12.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        f1.pack(fill=BOTH, expand=True, padx=10, pady=10)

        ###########################
        # Bottom Settings Page NavBar
        ###########################

        f2 = Frame(self, bg="pink", height=80)

        f21 = Frame(f2, bg="pink")
        Button(f21, width=20, font=('Lucida 20'), text="Admin Panel", command=lambda: self.controller.show_frame(
            Admin_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)

        f21.pack(side=LEFT, fill=Y, expand=True)

        f22 = Frame(f2, bg="pink")

        Button(f22, width=20, font=('Lucida 20'), text="Logout", command=lambda: self.controller.show_frame(
            Login_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)
        f22.pack(side=LEFT, fill=Y, expand=True)

        f23 = Frame(f2, bg="pink")
        Button(f23, width=20, font=('Lucida 20'), text="Exit", command=self.exit_app).pack(
            fill=BOTH, expand=True, padx=10, pady=10)
        f23.pack(side=LEFT, fill=Y, expand=True)

        f2.pack(anchor=S, fill=X, expand=True)
        f2.pack_propagate(0)

    def validatePassword(self):
        password = self.password.get()
        # print("password entered :",password )

        if not(len(password) == 0 or password == ''):
            if(self.db.check_admin_password(password)):
                # print('Authentication Successfull')
                self.ValidationText.set("")
                self.password.set('')
                return True

            else:
                self.password.set("")
                # print('Invalid Password')
                self.ValidationText.set("Invalid Password!!!")
                return False
        else:
            # print('Required Password')
            self.ValidationText.set("Password Required!!!")

    def toggle_fullscreen(self):

        if self.db.get_settings('fullscreen') == '1':
            self.db.set_settings('fullscreen', '0')
            self.master.master.master.attributes('-fullscreen', False)
            # self.master.master.master.state('normal')

        else:
            self.db.set_settings('fullscreen', '1')
            self.master.master.master.attributes('-fullscreen', True)

    def change_password(self):
        oldpassword = self.password.get()
        password = self.newpassword.get()
        retypepassword = self.retypenewpassword.get()

        if len(password) == 0 or password == "":
            self.ValidationText.set("New Password is Required")
            return False

        if len(password) <= 4:
            self.ValidationText.set(
                "New Password must contain more than 4 Characters")
            return False

        else:
            if(oldpassword == password):
                self.ValidationText.set(
                    "New Password cannot be same as Old one")
            else:

                if (retypepassword == password):

                    if self.validatePassword():
                        self.db.set_admin_password(password)
                        self.ValidationText.set("Password has been Changed")
                        self.newpassword.set('')
                        self.retypenewpassword.set('')

                    return True
                else:
                    self.ValidationText.set("New Passwords Do not Match")

        return False

    def reset_database(self):
        if self.validatePassword():
            self.ValidationText.set("")
            self.db.remake_database()
            self.controller.show_frame(Register_Frame)

    def delete_surveys(self):
        if self.validatePassword():
            self.ValidationText.set("All Surveys has been Deleted")
            self.db.clear_survey()

    def exit_app(self):
        self.master.master.master.destroy()
