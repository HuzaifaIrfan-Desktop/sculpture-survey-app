

from tkinter import * 
import tkinter as tk   


from tkinter import ttk
from functools import partial
from tkinter import messagebox


surveyformat={
    'sex':{
        1:'Male',
        2:'Female',
        3:'Others'
        },

    'ethnicity':{
        1:'White',
        2:'Black',
        3:'Chinese',
        4:'Asian',
        5:'Others',
        },

    'enjoyed':{
        1:'Not at all',
        2:'A little',
        3:'Moderately',
        4:'Very Much',
        5:'Extremely',
        },

}


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


        Label(f1,text="Last Name").pack()
        self.lastname = StringVar()
        Entry(f1, textvariable=self.lastname).pack()


        
        Label(f1,text="Age").pack()
        self.age = StringVar()
        Entry(f1, textvariable=self.age).pack()



        Label(f1,text="Sex").pack()
        f2 = Frame(f1)
        f2.pack()
        self.sexValue = IntVar()
        for key,value in surveyformat['sex'].items():
            Radiobutton(f2,text=value, value=key, variable=self.sexValue).grid(column=key, row=0)

        

        Label(f1,text="Ethnicity").pack()
        self.ethnicity = ttk.Combobox(f1, state="readonly")
        self.ethnicity['values']=('---',)
        for key, lst in surveyformat['ethnicity'].items():
            self.ethnicity['values'] = self.ethnicity['values'] + (lst,)
        self.ethnicity.current(0)
        self.ethnicity.pack()


        def clicked():
            print(self.firstname.get())
            print(self.lastname.get())

            age=self.age.get()
            print(age)
            if len(age)==0:
                self.ValidationText.set('Age Field can\'t be empty')
                return False
            else:
                try:
                    if int(age) < 0:
                        self.ValidationText.set('Age can\'t be negative')
                        return False                        

                except:
                    self.ValidationText.set('Age cannot be a string')
                    return False

            print(self.sexValue.get())

            def get_ethinicity_key(val):
                for key, value in surveyformat['ethnicity'].items():
                    if val == value:
                        return key
                return 0

            ethnicity=get_ethinicity_key(self.ethnicity.get())

            print(self.disbaledValue.get())
            print(self.enjoyedValue.get())
            print(self.curiousValue.get())
            print(self.scienceValue.get())
            
            
            


        Label(f1,text="Disbaled").pack()
        f3 = Frame(f1)
        f3.pack()
        self.disbaledValue = IntVar()
        Radiobutton(f3,text='Yes', value=1, variable=self.disbaledValue).grid(column=1, row=0)
        Radiobutton(f3,text='No', value=2, variable=self.disbaledValue).grid(column=2, row=0)


        Label(f1,text="Did you enjoy the sculpture?").pack()
        f4 = Frame(f1)
        f4.pack()
        self.enjoyedValue = IntVar()
        for key,value in surveyformat['enjoyed'].items():
            Radiobutton(f4,text=value, value=key, variable=self.enjoyedValue).grid(column=key, row=0)




        Label(f1,text="Are you curious about knowing more?").pack()
        f5 = Frame(f1)
        f5.pack()
        self.curiousValue = IntVar()
        Radiobutton(f5,text='Yes', value=1, variable=self.curiousValue).grid(column=1, row=0)
        Radiobutton(f5,text='No', value=2, variable=self.curiousValue).grid(column=2, row=0)

        
        Label(f1,text="Do you want to know more science behind it?").pack()
        f6 = Frame(f1)
        f6.pack()
        self.scienceValue = IntVar()
        Radiobutton(f6,text='Yes', value=1, variable=self.scienceValue).grid(column=1, row=0)
        Radiobutton(f6,text='No', value=2, variable=self.scienceValue).grid(column=2, row=0)



        Button(f1, text="Submit", command=clicked).pack()

        Button(f1, text="Clear", command=clicked).pack()

             
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(f1, textvariable=self.ValidationText).pack()
        self.ValidationText.set("")



  






















        # # Initialize frames
        # f1 = Frame(self.user_tab, bg="grey")
        # f2 = Frame(self.user_tab, bg="pink")

        # # Initialize labels
        # w1 = Label(f1, text="Red", bg="red", fg="white")
        # w2 = Label(f1, text="Yellow", bg="yellow", fg="white")
        # w3 = Label(f1, text="Green", bg="green", fg="white")
        # w1b = Label(f2, text="Red", bg="red", fg="white")
        # w2b = Label(f2, text="Yellow", bg="yellow", fg="white")
        # w3b = Label(f2, text="Green", bg="green", fg="white")

        # # Packing level 1
        # f1.pack(fill=BOTH, expand=True)
        # f2.pack(fill=BOTH, expand=True)

        # # Packing level 2
        # w1.pack(fill=BOTH, expand=True)
        # w2.pack(fill=BOTH, expand=True)
        # w3.pack(fill=BOTH, expand=True)
        # w1b.pack(side=LEFT, fill=BOTH, expand=True)
        # w2b.pack(side=LEFT, fill=BOTH, expand=True)
        # w3b.pack(side=LEFT, fill=BOTH, expand=True)

