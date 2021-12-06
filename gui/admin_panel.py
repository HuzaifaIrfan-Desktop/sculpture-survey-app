from tkinter import * 
from tkinter import filedialog

import tkinter as tk   
from tkinter import ttk
from functools import partial
import os
from .survey_format import survey_format
import csv


class Admin_Panel(Frame):

    def __init__(self, parent, tabControl,db):
        super().__init__(parent)
        self.db=db



        self.admin_tab = Frame(tabControl)
        tabControl.add(self.admin_tab, text ='Admin Panel')

        
        self.admin_tab.grid_rowconfigure(0, weight=1) 
        self.admin_tab.grid_columnconfigure(0, weight=1) 


        # self.admin_tab.configure(background='black')


        self.frames = {}
        for F in (Register_Frame,Login_Frame,Admin_Frame,Settings_Frame):
            frame = F(self.admin_tab,self, db)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_rowconfigure(0, weight = 1)
            frame.grid_columnconfigure(0, weight = 1)





        if(self.db.empty_admin_password()):
            self.show_frame(Register_Frame)
            print('RegisterPage')
        else:
            self.show_frame(Login_Frame)
            print('LoginPage') 

        self.show_frame(Admin_Frame)   

    def show_frame(self,container):
        frame = self.frames[container]
        frame.tkraise()


class Register_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller

        self.admin_tab=parent

        
        
        Label(self, text="Register", font=('Lucida 15')).pack()


        
        f1 = Frame(self, bg="grey")
        f1.pack(fill=BOTH, expand=True)


        #password label and password entry box
        self.passwordLabel = Label(f1,text="Password")
        self.passwordLabel.pack()
        self.password = StringVar()
        self.passwordTextbox = Entry(f1, textvariable=self.password, show='*')
        self.passwordTextbox.pack()

        self.retypepasswordLabel = Label(f1,text="Retype Password")
        self.retypepasswordLabel.pack()
        self.retypepassword = StringVar()
        self.retypepasswordTextbox = Entry(f1, textvariable=self.retypepassword, show='*')
        self.retypepasswordTextbox.pack()

        validateRegister = partial(self.validateRegister, self.password,self.retypepassword)

        #login button
        self.loginButton = Button(f1, text="Create Admin Password", command=validateRegister)
        self.loginButton.pack()

     
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(f1, textvariable=self.ValidationText)
        
        self.ValidationLabel.pack()

    def validateRegister(self, passwd,retypepasswd):
        password=passwd.get()
        retypepassword=retypepasswd.get()

        

        if len(password)==0:
            self.ValidationText.set("Password is Required")
            return False

        if len(password)<=4:
            self.ValidationText.set("Password must contain more than 4 Characters")
            return False
        else:
            if (retypepassword==password):
                self.db.set_admin_password(password)
                self.controller.show_frame(Admin_Frame)
                self.password.set('')
                self.retypepassword.set('')

                return True
            else:
                self.ValidationText.set("Password Do not Match")


        return False


class Login_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller


        
        f1 = Frame(self)
        f1.place(anchor="c", relx=.5, rely=.5)
        # f1.pack(fill=BOTH, expand=True)

        self.configure(background='black')


        Label(f1, text="Login Page", font=('Lucida 15')).pack()

        #password label and password entry box
        self.passwordLabel = Label(f1,text="Password").pack()
        self.password = StringVar()
        self.passwordEntry = Entry(f1, textvariable=self.password, show='*').pack()

        validateLogin = partial(self.validateLogin, self.password)
        #login button
        self.loginButton = Button(f1, text="Login", command=validateLogin).pack()


     
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(f1, textvariable=self.ValidationText).pack()
        self.ValidationText.set("")

    
        
    def validateLogin(self, passwd):
        password=passwd.get()

        if len(password)==0:
            self.ValidationText.set("Please Enter your Password")
            return False

        # print("password entered :",password )


        if(self.db.check_admin_password(password)):
            print('Login Successful')
            self.ValidationText.set("")
            self.password.set('')
            self.controller.show_frame(Admin_Frame)
            return True

        else:
            print('Invalid Password')
            self.ValidationText.set("Invalid Password")
            return False







class Admin_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller

        self.admin_tab=parent
        Label(self, text="Admin Panel", font=('Lucida 15')).pack()




        f3 = Frame(self, bg="pink")
        f3.pack(fill=BOTH, expand=True)

        




        self.headings = ('ID', 'Firstname', 'Lastname', 'Age', 'Gender', 'Ethnicity', 'Disabled', 'Enjoyed', 'Curious', 'Want to know more Science',)
        


        #     print("Id: ", survey[0])
        #     print("firstname: ", survey[1])
        #     print("lastname: ", survey[2])
        #     print("age: ", survey[3])
        #     print("gender: ", survey[4])
        #     print("ethnicity: ", survey[5])
        #     print("disbaledValue: ", survey[6])
        #     print("enjoyedValue: ", survey[7])
        #     print("curiousValue: ", survey[8])
        #     print("scienceValue: ", survey[9])
 

        label = tk.Label(f3, text="Surveys", font=("Arial",30)).pack(fill=X, expand=False)
        # create Treeview with 3 columns
        self.listBox = ttk.Treeview(f3, columns=self.headings, show='headings')
        self.listBox.column(1, anchor=CENTER, stretch=NO, width=50)
        # set column headings
        for n, col in enumerate(self.headings):
            self.listBox.column(n, anchor=CENTER, stretch=NO, width=100)
            self.listBox.heading(col, text=col) 
        self.listBox.column(0, anchor=CENTER, stretch=NO, width=50)  
        self.listBox.column(9, anchor=CENTER, stretch=NO, width=170)   
        self.listBox.pack(fill=BOTH, expand=True)
        # self.listBox.grid_configure(padx=10, pady=10)







        # Initialize frames
        f1 = Frame(self, bg="pink")
        f2 = Frame(self, bg="pink")

        # Initialize labels
        w1 = Frame(f1, bg="pink")
        w2 = Frame(f1, bg="pink")
        w3 = Frame(f1, bg="pink")


        # Packing level 1
        f1.pack(fill=BOTH, expand=True)
        f2.pack(fill=BOTH, expand=True)

        # Packing level 2
        w1.pack(fill=BOTH, expand=True, padx=10, pady=10)
        w2.pack(fill=BOTH, expand=True)
        w3.pack(fill=BOTH, expand=True)

        

        Label(w1, text='Average Age').pack(side=LEFT)
        self.AverageAgeText = StringVar(value="")
        Label(w1, textvariable=self.AverageAgeText).pack(side=LEFT)

        Label(w1, text='Average Age').pack(side=LEFT)
        self.AverageAgeText = StringVar(value="")
        Label(w1, textvariable=self.AverageAgeText).pack(side=LEFT)

        Label(w1, text='Average Age').pack(side=LEFT)
        self.AverageAgeText = StringVar(value="")
        Label(w1, textvariable=self.AverageAgeText).pack(side=LEFT)

        Button(w2, text="Refresh", width=15, command=self.refresh_data).pack(fill=BOTH, expand=True, padx=10, pady=10)

        Button(w3, text="Save as CSV", width=15, command=self.ask_file_save).pack(fill=BOTH, expand=True,padx=10, pady=10)



        # self.ValidationText = StringVar(value="")
        # self.ValidationLabel = Label(self, textvariable=self.ValidationText).pack()

        w1b = Frame(f2, bg="pink")
        w2b = Frame(f2, bg="pink")
        w3b = Frame(f2, bg="pink")

        self.settingsButton = Button(w1b, text="Settings", command=lambda : self.controller.show_frame(Settings_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)


        #Logout button
        self.logoutButton = Button(w2b, text="Logout", command=lambda : self.controller.show_frame(Login_Frame)).pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.exitButton = Button(w3b, text="Exit", command= self.exit_app).pack(fill=BOTH, expand=True, padx=10, pady=10)
        w1b.pack(side=LEFT, fill=BOTH, expand=True)
        w2b.pack(side=LEFT, fill=BOTH, expand=True)
        w3b.pack(side=LEFT, fill=BOTH, expand=True)


        self.surveys=[]

        # self.refresh_data()
  


    def refresh_data(self):

        self.surveys = self.db.get_all_surveys()



        age_list = []
        for n, survey in enumerate(self.surveys):
            asurvey=list(survey)
            
            age_list.append(survey[3])
            asurvey[4]=survey_format['gender']['values'][survey[4]]
            asurvey[5]=survey_format['ethnicity']['values'][survey[5]]
            asurvey[6]=survey_format['disabled']['values'][survey[6]]
            asurvey[7]=survey_format['enjoyed']['values'][survey[7]]
            asurvey[8]=survey_format['curious']['values'][survey[8]]
            asurvey[9]=survey_format['science']['values'][survey[9]]
            self.surveys[n]=asurvey

        self.average_age = (sum(age_list))/len(age_list)


        self.AverageAgeText.set(self.average_age)


        # self.surveys.sort(key=lambda e: e[1], reverse=True)
        self.listBox.delete(*self.listBox.get_children())

        for i, args in enumerate(self.surveys, start=1):
            self.listBox.insert("", "end", values=(*args,))





    def ask_file_save(self):
        data = self.surveys
        
        file_name =tk.filedialog.asksaveasfilename(initialdir = "",title = "Save as CSV",filetypes = (("CSV file","*.csv"),),)
        # print (file_name)
        self.master.master.master.bring_to_front()
        if (file_name == None or file_name == ''):
            return

        if(not file_name.endswith(".csv")):
            file_name=file_name+'.csv'

        self.save_csv(file_name,self.headings, data)
        # print('Saved Csv')
        

    def save_csv(self,file_name,headings, data):
        with open(file_name, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows(data)


    def exit_app(self):
        print('Exitted')
        self.master.master.master.destroy()
            








class Settings_Frame(Frame):

    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.db=db
        self.controller=controller


        self.admin_tab=parent

        Label(self, text="Settings", font=('Lucida 15')).pack()


        #Logout button
        self.logoutButton = Button(self, text="Logout", command=lambda : self.controller.show_frame(Login_Frame)).pack()

        self.adminButton = Button(self, text="Admin Panel", command=lambda : self.controller.show_frame(Admin_Frame)).pack()


        self.passwordLabel = Label(self,text="Password").pack()
        self.password = StringVar()
        self.passwordTextbox = Entry(self, textvariable=self.password, show='*').pack()

        self.changepasswordLabel = Label(self,text="Change Password").pack()

        self.newpasswordLabel = Label(self,text="New Password").pack()
        self.newpassword = StringVar()
        self.newpasswordTextbox = Entry(self, textvariable=self.newpassword, show='*').pack()

        self.retypenewpasswordLabel = Label(self,text="Retype New Password").pack()
        self.retypenewpassword = StringVar()
        self.retypenewpasswordTextbox = Entry(self, textvariable=self.retypenewpassword, show='*').pack()

        changepassword = partial(self.changepassword, self.password,self.newpassword,self.retypenewpassword)
        self.changepassword_Button = Button(self, text="Change Password", command=changepassword).pack()





        self.DangerLabel = Label(self,text="Danger").pack()


        resetdatabase = partial(self.resetdatabase, self.password)
        self.resetdatabase_Button = Button(self, text="Reset Database", command=resetdatabase).pack()

        deletesurveys = partial(self.deletesurveys, self.password)
        self.deletesurveys_Button = Button(self, text="Delete Surveys", command=deletesurveys).pack()


     
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(self, textvariable=self.ValidationText).pack()

    def validatePassword(self, passwd):
        password=passwd.get()
        # print("password entered :",password )
        if(self.db.check_admin_password(password)):
            print('Login Successful')
            self.ValidationText.set("")
            self.password.set('')
            return True

        else:
            print('Invalid Password')
            self.ValidationText.set("Password is Required!!!")
            return False

    def changepassword(self,passwd, newpasswd,retypenewpasswd):
        if self.validatePassword(passwd):
            self.ValidationText.set("")
            self.setnewpassword(passwd, newpasswd,retypenewpasswd)

    def setnewpassword(self,oldpasswd, passwd,retypepasswd):
        oldpassword=oldpasswd.get()
        password=passwd.get()
        retypepassword=retypepasswd.get()
        # print("password entered :",password )
        # print("password entered :",retypepassword )
        

        if len(password)==0:
            self.ValidationText.set("New Password is Required")
            return False

        if len(password)<=4:
            self.ValidationText.set("New Password must contain more than 4 Characters")
            return False
        else:
            if(oldpassword==password):
                self.ValidationText.set("New Password cannot be same as Old one")
            else:

                if (retypepassword==password):
                    self.db.set_admin_password(password)
                    self.ValidationText.set("Password has been Changed")
                    self.newpassword.set('')
                    self.retypenewpassword.set('')
                    

                    return True
                else:
                    self.ValidationText.set("New Passwords Do not Match")


        return False

    def resetdatabase(self,passwd):
        if self.validatePassword(passwd):
            self.ValidationText.set("")
            self.db.remake_database()
            self.controller.show_frame(Register_Frame)

    def deletesurveys(self,passwd):
        if self.validatePassword(passwd):
            self.ValidationText.set("All Surveys has been Deleted")
            self.db.clear_survey()


    

