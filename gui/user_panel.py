

#################################################################################
####################  User Panel Class ##########################################
#################################################################################


from tkinter import *
import tkinter as tk


from tkinter import ttk
from functools import partial
from tkinter import messagebox
from .survey_format import survey_format
from pathlib import Path

ASSETS_PATH = Path(__file__).resolve().parent / "assets"


class User_Panel(Frame):

    def __init__(self, parent, tabControl, db):
        super().__init__(parent)
        self.db = db

        self.user_tab = Frame(tabControl)
        tabControl.add(self.user_tab, text='Singing Sculpture Survey')
        self.user_tab.configure(background="#3A7FF6")

        f1 = Frame(self.user_tab, bg="#3A7FF6")

        Label(f1, bg="#3A7FF6", text="Singing Sculpture Survey",
              font=("Arial 30 bold")).pack(side='top')

        Label(f1, font=('Lucida 15 bold'), bg="#3A7FF6",
              text="Your feedback helps us improve your experience.").pack()

        f11 = Frame(f1, bg="#3A7FF6")

        Label(f11, font=('Lucida 10 bold'),
              bg="#3A7FF6", text="First Name").pack()
        self.firstname = StringVar()
        Entry(f11, font=('Lucida 10'),
              textvariable=self.firstname).pack(pady=(0, 5))

        def firstname_validation(*args):
            firstnamestr = self.firstname.get()
            valid_firstname = ""
            for ch in firstnamestr:
                if((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch == ' '):
                    if len(valid_firstname) <= 15:
                        valid_firstname = valid_firstname+ch

            self.firstname.set(valid_firstname)
        self.firstname.trace("w", firstname_validation)

        Label(f11, font=('Lucida 10 bold'),
              bg="#3A7FF6", text="Last Name").pack()
        self.lastname = StringVar()
        Entry(f11, font=('Lucida 10'),
              textvariable=self.lastname).pack(pady=(0, 5))

        def lastname_validation(*args):
            lastnamestr = self.lastname.get()
            valid_lastname = ""
            for ch in lastnamestr:
                if((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch == ' '):
                    if len(valid_lastname) <= 15:
                        valid_lastname = valid_lastname+ch

            self.lastname.set(valid_lastname)
        self.lastname.trace("w", lastname_validation)

        Label(f11, font=('Lucida 10 bold'), bg="#3A7FF6", text="Age").pack()
        self.age = StringVar()
        Entry(f11, font=('Lucida 10'), textvariable=self.age).pack(pady=(0, 5))

        def age_validation(*args):
            agestr = self.age.get()
            valid_age = ""
            for ch in agestr:
                try:
                    int(ch)
                    if len(valid_age) < 3:
                        valid_age = valid_age+ch
                except:
                    pass

            self.age.set(valid_age)
        self.age.trace("w", age_validation)

        Label(f11, font=('Lucida 10 bold'), bg="#3A7FF6", text="Gender").pack()
        f111 = Frame(f11, bg="#3A7FF6")

        self.gender = IntVar()
        for key, value in survey_format['gender']['values'].items():
            Radiobutton(f111, font=('Lucida 10'), bg="#3A7FF6", text=value,
                        value=key, variable=self.gender).grid(column=key, row=0)

        f111.pack(pady=(0, 5))

        Label(f11, font=('Lucida 10 bold'),
              bg="#3A7FF6", text="Ethnicity").pack()
        self.ethnicity = ttk.Combobox(
            f11, font=('Lucida 10'), state="readonly")
        self.ethnicity['values'] = ('---',)
        for key, lst in survey_format['ethnicity']['values'].items():
            self.ethnicity['values'] = self.ethnicity['values'] + (lst,)
        self.ethnicity.current(0)
        self.ethnicity.pack(pady=(0, 5))

        Label(f11, font=('Lucida 10 bold'),
              bg="#3A7FF6", text="Disabled").pack()
        f112 = Frame(f11, bg="#3A7FF6")

        self.disabled = IntVar()
        for key, value in survey_format['disabled']['values'].items():
            Radiobutton(f112, font=('Lucida 10'), bg="#3A7FF6", text=value,
                        value=key, variable=self.disabled).grid(column=key, row=0)

        f112.pack(pady=(0, 5))

        Label(f11, font=('Lucida 10 bold'), bg="#3A7FF6",
              text="Did you enjoy the sculpture?").pack()
        f113 = Frame(f11, bg="#3A7FF6")

        self.enjoyed = IntVar()
        for key, value in survey_format['enjoyed']['values'].items():
            Radiobutton(f113, font=('Lucida 10'), bg="#3A7FF6", text=value,
                        value=key, variable=self.enjoyed).grid(column=key, row=0)

        f113.pack(pady=(0, 5))

        Label(f11, font=('Lucida 10 bold'), bg="#3A7FF6",
              text="Are you curious about knowing more?").pack()
        f114 = Frame(f11, bg="#3A7FF6")

        self.curious = IntVar()
        for key, value in survey_format['curious']['values'].items():
            Radiobutton(f114, font=('Lucida 10'), bg="#3A7FF6", text=value,
                        value=key, variable=self.curious).grid(column=key, row=0)

        f114.pack(pady=(0, 5))

        Label(f11, font=('Lucida 10 bold'), bg="#3A7FF6",
              text="Do you want to know more science behind it?").pack()
        f115 = Frame(f11, bg="#3A7FF6")

        self.science = IntVar()
        for key, value in survey_format['science']['values'].items():
            Radiobutton(f115, font=('Lucida 10'), bg="#3A7FF6", text=value,
                        value=key, variable=self.science).grid(column=key, row=0)

        f115.pack(pady=(0, 5))

        f116 = Frame(f11, bg="#3A7FF6")

        Button(f116, font=('Lucida 15'), text="Submit",
               command=self.submit_survey).pack(side=LEFT, padx=10)

        Button(f116, font=('Lucida 15'), text="Clear",
               command=self.clear_form).pack(side=LEFT, padx=10)
        f116.pack(pady=10)

        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(f11, font=(
            'Lucida 10'), bg="#3A7FF6", textvariable=self.ValidationText).pack()
        self.ValidationText.set("")

        f11.pack(side=LEFT, padx=20, pady=20)

        f1.pack(fill=BOTH, side=LEFT, padx=20, pady=20)

        f3 = Frame(self.user_tab)

        f3.picture = PhotoImage(file=ASSETS_PATH / "survey_bg.png")

        Label(f3, image=f3.picture).pack(expand=True)

        f3.pack(expand=True)

    def clear_form(self):

        self.ValidationText.set('')

        self.firstname.set('')
        self.lastname.set('')
        self.age.set('')
        self.gender.set(0)
        self.ethnicity.set('---')
        self.disabled.set(0)
        self.enjoyed.set(0)

        self.curious.set(0)
        self.science.set(0)

    def submit_survey(self):
        firstname = self.firstname.get()
        # print(firstname)
        if len(firstname) == 0:
            self.ValidationText.set('First Name Field can\'t be empty')
            return False

        lastname = self.lastname.get()
        # print(lastname)
        if len(lastname) == 0:
            self.ValidationText.set('Last Name Field can\'t be empty')
            return False

        age = self.age.get()
        # print(age)
        if len(age) == 0:
            self.ValidationText.set('Age Field can\'t be empty')
            return False
        else:
            age = int(age)

            if age == 0:
                self.ValidationText.set('Age can\'t be zero')
                return False

        gender = self.gender.get()
        # print(gender)
        if gender == 0:
            self.ValidationText.set('Please Select your Gender')
            return False

        def get_ethinicity_key(val):
            for key, value in survey_format['ethnicity']['values'].items():
                if val == value:
                    return key
            return 0

        ethnicity = get_ethinicity_key(self.ethnicity.get())
        if ethnicity == 0:
            self.ValidationText.set('Please Select your Ethnicity')
            return False

        disabled = self.disabled.get()
        # print(disabled)
        if disabled == 0:
            self.ValidationText.set('Please fill all fields')
            return False

        enjoyed = self.enjoyed.get()
        # print(enjoyed)
        if enjoyed == 0:
            self.ValidationText.set('Please fill all fields')
            return False

        curious = self.curious.get()
        # print(curious)
        if curious == 0:
            self.ValidationText.set('Please fill all fields')
            return False

        science = self.science.get()
        # print(science)
        if science == 0:
            self.ValidationText.set('Please fill all fields')
            return False

        self.clear_form()
        self.ValidationText.set('Form Submitted Thank You for your Time.')

        self.db.save_survey(firstname, lastname, age, gender,
                            ethnicity, disabled, enjoyed, curious, science)
