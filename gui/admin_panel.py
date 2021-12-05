
from tkinter import * 
import tkinter as tk                 
from tkinter import ttk
from functools import partial


class Admin_Panel():

    def __init__(self, parent, tabControl,db):
        self.db=db
      
        self.admin_tab = ttk.Frame(tabControl)
        tabControl.add(self.admin_tab, text ='Admin Panel')

        self.frames = {}
        for F in (Register_Frame,Login_Frame,Admin_Frame,Settings_Frame):
            frame = F(self.admin_tab,self, db)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')





        if(self.db.empty_admin_password()):
            self.show_frame(Register_Frame)
            print('RegisterPage')
        else:
            self.show_frame(Login_Frame)
            print('LoginPage')     

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


        #password label and password entry box
        self.passwordLabel = Label(self,text="Password")
        self.passwordLabel.pack()
        self.password = StringVar()
        self.passwordTextbox = Entry(self, textvariable=self.password, show='*')
        self.passwordTextbox.pack()

        self.retypepasswordLabel = Label(self,text="Retype Password")
        self.retypepasswordLabel.pack()
        self.retypepassword = StringVar()
        self.retypepasswordTextbox = Entry(self, textvariable=self.retypepassword, show='*')
        self.retypepasswordTextbox.pack()

        validateRegister = partial(self.validateRegister, self.password,self.retypepassword)

        #login button
        self.loginButton = Button(self, text="Create Admin Password", command=validateRegister)
        self.loginButton.pack()

     
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(self, textvariable=self.ValidationText)
        
        self.ValidationLabel.pack()

    def validateRegister(self, passwd,retypepasswd):
        password=passwd.get()
        retypepassword=retypepasswd.get()
        print("password entered :",password )
        print("password entered :",retypepassword )
        

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

        Label(self, text="Login Page", font=('Lucida 15')).pack()

        #password label and password entry box
        self.passwordLabel = Label(self,text="Password").pack()
        self.password = StringVar()
        self.passwordEntry = Entry(self, textvariable=self.password, show='*').pack()

        validateLogin = partial(self.validateLogin, self.password)
        #login button
        self.loginButton = Button(self, text="Login", command=validateLogin).pack()


     
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(self, textvariable=self.ValidationText).pack()
        self.ValidationText.set("Error")

    
        
    def validateLogin(self, passwd):
        password=passwd.get()

        if len(password)==0:
            self.ValidationText.set("Please Enter your Password")
            return False

        print("password entered :",password )


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


        #Logout button
        self.logoutButton = Button(self, text="Logout", command=lambda : self.controller.show_frame(Login_Frame)).pack()

        self.settingsButton = Button(self, text="Settings", command=lambda : self.controller.show_frame(Settings_Frame)).pack()

     
        self.ValidationText = StringVar(value="")
        self.ValidationLabel = Label(self, textvariable=self.ValidationText).pack()


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
        print("password entered :",password )
        if(self.db.check_admin_password(password)):
            print('Login Successful')
            self.ValidationText.set("")
            self.password.set('')
            return True

        else:
            print('Invalid Password')
            self.ValidationText.set("Invalid Password")
            return False

    def changepassword(self,passwd, newpasswd,retypenewpasswd):
        if self.validatePassword(passwd):
            self.ValidationText.set("")
            self.setnewpassword(passwd, newpasswd,retypenewpasswd)

    def setnewpassword(self,oldpasswd, passwd,retypepasswd):
        oldpassword=oldpasswd.get()
        password=passwd.get()
        retypepassword=retypepasswd.get()
        print("password entered :",password )
        print("password entered :",retypepassword )
        

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
            



