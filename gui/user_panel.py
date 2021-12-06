

from tkinter import * 
import tkinter as tk   


from tkinter import ttk
from functools import partial
from tkinter import messagebox
from .survey_format import survey_format

class User_Panel(Frame):

    def __init__(self, parent, tabControl,db):
        super().__init__(parent)
        self.db=db


        self.user_tab = Frame(tabControl)
        tabControl.add(self.user_tab, text ='Survey Form')


        Label(self.user_tab, text="Survey Form", font=('Lucida 15')).pack(side='top')
        
        f1 = Frame(self.user_tab)
        f1.pack()

        Label(f1,text="Your feedback helps us improve your experience.").pack()


        Label(f1,text="Name").pack()

       
        Label(f1,text="First Name").pack()
        self.firstname = StringVar()
        Entry(f1, textvariable=self.firstname).pack()
        def firstname_validation(*args):
            firstnamestr=self.firstname.get()
            valid_firstname=""
            for ch in firstnamestr:
                if((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch==' '): 
                    if len(valid_firstname)<=15:
                        valid_firstname=valid_firstname+ch
    
            self.firstname.set(valid_firstname)
        self.firstname.trace("w", firstname_validation)



        Label(f1,text="Last Name").pack()
        self.lastname = StringVar()
        Entry(f1, textvariable=self.lastname).pack()

        def lastname_validation(*args):
            lastnamestr=self.lastname.get()
            valid_lastname=""
            for ch in lastnamestr:
                if((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch==' '): 
                    if len(valid_lastname)<=15:
                        valid_lastname=valid_lastname+ch
    
            self.lastname.set(valid_lastname)
        self.lastname.trace("w", lastname_validation)


        Label(f1,text="Age").pack()
        self.age = StringVar()
        Entry(f1, textvariable=self.age).pack()
        def age_validation(*args):
            agestr=self.age.get()
            valid_age=""
            for ch in agestr:
                try:
                    int(ch)
                    if len(valid_age)<3:
                        valid_age=valid_age+ch
                except:
                    pass

            self.age.set(valid_age)
        self.age.trace("w", age_validation)



        Label(f1,text="Gender").pack()
        f2 = Frame(f1)
        f2.pack()
        self.gender = IntVar()
        for key,value in survey_format['gender']['values'].items():
            Radiobutton(f2,text=value, value=key, variable=self.gender).grid(column=key, row=0)

        

        Label(f1,text="Ethnicity").pack()
        self.ethnicity = ttk.Combobox(f1, state="readonly")
        self.ethnicity['values']=('---',)
        for key, lst in survey_format['ethnicity']['values'].items():
            self.ethnicity['values'] = self.ethnicity['values'] + (lst,)
        self.ethnicity.current(0)
        self.ethnicity.pack()


    
            
            


        Label(f1,text="Disbaled").pack()
        f3 = Frame(f1)
        f3.pack()
        self.disbaledValue = IntVar()
        for key,value in survey_format['disabled']['values'].items():
            Radiobutton(f3,text=value, value=key, variable=self.disbaledValue).grid(column=key, row=0)



        Label(f1,text="Did you enjoy the sculpture?").pack()
        f4 = Frame(f1)
        f4.pack()
        self.enjoyedValue = IntVar()
        for key,value in survey_format['enjoyed']['values'].items():
            Radiobutton(f4,text=value, value=key, variable=self.enjoyedValue).grid(column=key, row=0)




        Label(f1,text="Are you curious about knowing more?").pack()
        f5 = Frame(f1)
        f5.pack()
        self.curiousValue = IntVar()
        for key,value in survey_format['curious']['values'].items():
            Radiobutton(f5,text=value, value=key, variable=self.curiousValue).grid(column=key, row=0)

        
        Label(f1,text="Do you want to know more science behind it?").pack()
        f6 = Frame(f1)
        f6.pack()
        self.scienceValue = IntVar()
        for key,value in survey_format['science']['values'].items():
            Radiobutton(f6,text=value, value=key, variable=self.scienceValue).grid(column=key, row=0)



        Button(f1, text="Submit", command=self.submit_survey).pack()

        Button(f1, text="Clear", command=self.clear_form).pack()

             
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(f1, textvariable=self.ValidationText).pack()
        self.ValidationText.set("")



    def clear_form(self):

        self.ValidationText.set('')

        self.firstname.set('')
        self.lastname.set('')
        self.age.set('')
        self.gender.set(0)
        self.ethnicity.set('---')
        self.disbaledValue.set(0)
        self.enjoyedValue.set(0)

        self.curiousValue.set(0)
        self.scienceValue.set(0)

        

  

    def submit_survey(self):
        firstname=self.firstname.get()
        # print(firstname)
        if len(firstname)==0:
            self.ValidationText.set('First Name Field can\'t be empty')
            return False
            
        lastname=self.lastname.get()
        # print(lastname)
        if len(lastname)==0:
            self.ValidationText.set('Last Name Field can\'t be empty')
            return False

        age=self.age.get()
        # print(age)
        if len(age)==0:
            self.ValidationText.set('Age Field can\'t be empty')
            return False
        else:
            age=int(age)

            if age == 0:
                self.ValidationText.set('Age can\'t be zero')
                return False




        gender=self.gender.get()
        # print(gender)
        if gender==0:
            self.ValidationText.set('Please Select your Gender')
            return False

        def get_ethinicity_key(val):
            for key, value in survey_format['ethnicity']['values'].items():
                if val == value:
                    return key
            return 0

        ethnicity=get_ethinicity_key(self.ethnicity.get())
        if ethnicity==0:
            self.ValidationText.set('Please Select your Ethnicity')
            return False


        disbaledValue=self.disbaledValue.get()
        # print(disbaledValue)
        if disbaledValue==0:
            self.ValidationText.set('Please fill all fields')
            return False


        enjoyedValue=self.enjoyedValue.get()
        # print(enjoyedValue)
        if enjoyedValue==0:
            self.ValidationText.set('Please fill all fields')
            return False



        curiousValue=self.curiousValue.get()
        # print(curiousValue)
        if curiousValue==0:
            self.ValidationText.set('Please fill all fields')
            return False


        scienceValue=self.scienceValue.get()
        # print(scienceValue)
        if scienceValue==0:
            self.ValidationText.set('Please fill all fields')
            return False

        
        
        self.clear_form()
        self.ValidationText.set('Form Submitted Thank You for your Time.')
        
        self.db.save_survey(firstname,lastname,age,gender,ethnicity,disbaledValue,enjoyedValue,curiousValue,scienceValue)


        










