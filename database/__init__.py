import sqlite3
import hashlib
import os

class Database:


    def __init__(self,database_filename):    

        self.location = database_filename
        self.conn = sqlite3.connect(self.location)
        self.c = self.conn.cursor()
        self.survey_table = 'survey'
        self.admin_table = 'admin'
        self.settings_table = 'settings'
        

        # self.clear_database()
        self.create_database()

###########################
## Database functions
###########################

    def create_database(self):

        ## Survey Table
        sql = 'create table if not exists ' + self.survey_table + ''' 
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  firstname varchar(20) NOT NULL,
                  lastname varchar(20) NOT NULL,
                  age int NOT NULL,
                  gender int NOT NULL,
                  ethnicity int NOT NULL,
                  disabled int NOT NULL,
                  enjoyed int NOT NULL,
                  curious int NOT NULL,
                  science int NOT NULL)

        '''   
        self.c.execute(sql)

        ## Settings Table

        sql = 'create table if not exists ' + self.settings_table + ''' 
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  key varchar(20) UNIQUE NOT NULL,
                  value varchar(20) NOT NULL)
        '''   
        self.c.execute(sql)

        ## Admin Passwords Table

        sql = 'create table if not exists ' + self.admin_table + ''' 
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  salt varchar(64) NOT NULL,  
                  key varchar(256) NOT NULL)
        '''


        self.c.execute(sql)
        self.conn.commit()



    def drop_tables(self):
        ## Delete All Tables
        sql = 'drop table IF EXISTS ' + self.survey_table
        self.c.execute(sql)
        sql = 'drop table IF EXISTS ' + self.settings_table
        self.c.execute(sql)
        sql = 'drop table IF EXISTS ' + self.admin_table
        self.c.execute(sql)
        self.conn.commit()

        
    
    def remake_database(self):
        ## Delete and Create All Tables
        self.drop_tables()
        self.create_database()


    def clear_survey(self):
        ## Empty Survey Table
        self.c.execute('DELETE FROM '+self.survey_table)
        self.conn.commit()


###########################
## Survey Table Functions
###########################


    def save_survey(self, firstname, lastname, age, gender, ethnicity, disabled, enjoyed, curious, science):
        ## Insert a Survey in Survey Table
        sql = 'insert into ' + self.survey_table + f'''
        (firstname, lastname, age, gender, ethnicity, disabled, enjoyed, curious, science) values ("{firstname}", "{lastname}", {age}, {gender}, {ethnicity}, {disabled}, {enjoyed}, {curious}, {science})
        
        '''
        self.c.execute(sql)
        # print('Inserted ', firstname, lastname, age, gender, ethnicity, disabled, enjoyed, curious, science)
        self.conn.commit()

    def get_all_surveys(self):
        ## Get all Surveys from Survey Table
        cursor = self.c.execute(f'select * from {self.survey_table};')
        records = cursor.fetchall()
        # print("Total rows are:  ", len(records))

        return records

    

    ## Statistical Count Survey Table


    def get_gender_count(self,gender):
        self.c.execute(f"select count() from {self.survey_table} where gender={gender}")
        return int(self.c.fetchone()[0])

    def get_ethnicity_count(self,ethnicity):
        self.c.execute(f"select count() from {self.survey_table} where ethnicity={ethnicity}")
        return int(self.c.fetchone()[0])

    def get_disabled_count(self,disabled):
        self.c.execute(f"select count() from {self.survey_table} where disabled={disabled}")
        return int(self.c.fetchone()[0])

    def get_enjoyed_count(self,enjoyed):
        self.c.execute(f"select count() from {self.survey_table} where enjoyed={enjoyed}")
        return int(self.c.fetchone()[0])

    def get_curious_count(self,curious):
        self.c.execute(f"select count() from {self.survey_table} where curious={curious}")
        return int(self.c.fetchone()[0])

    def get_science_count(self,science):
        self.c.execute(f"select count() from {self.survey_table} where science={science}")
        return int(self.c.fetchone()[0])

###########################
## Settings Table Functions
###########################

    def set_settings(self,key,value):

        self.c.execute(f'''INSERT OR REPLACE INTO {self.settings_table} (key, value) VALUES("{key}", "{value}");''')
        self.conn.commit()

    
        
    def get_settings(self,key):
        self.c.execute(f"select (value) from {self.settings_table} where key='{key}'")
        try:
            return(self.c.fetchone()[0])
        except:
             self.set_settings(key,'1')
             return '1'



###########################
## Admin Table Functions
###########################

    def clear_admin_password(self):
        self.c.execute('DELETE FROM '+self.admin_table)
        self.conn.commit()


    def check_admin_password(self,password):
        cursor = self.c.execute(f'select * from {self.admin_table};')
        for passwd in cursor.fetchall():
            
            ## Convert to Bytes
            salt=bytes.fromhex(passwd[1])   
            # print(salt)
            key=bytes.fromhex(passwd[2])   
            # print(key)

            
            new_key = hashlib.pbkdf2_hmac(
                'sha256', # The hash digest algorithm for HMAC
                password.encode('utf-8'), # Convert the password to bytes
                salt, # Provide the salt
                100000, # It is recommended to use at least 100,000 iterations of SHA-256 
                dklen=128 # Get a 128 byte key
            )
            # print(new_key)



            ## Check key Match
            if(key==new_key):

                return True
        
        return False



    def set_admin_password(self,password):
        self.clear_admin_password()

        salt = os.urandom(32)
        

        ## Encrypt Password

        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256 
            dklen=128 # Get a 128 byte key
        )
        # print(salt)
        # print(key)


        ## Convert to Hex and Save 
        sql = f'''
        INSERT INTO {self.admin_table} (salt,key)
VALUES ("{salt.hex()}", "{key.hex()}");
        '''
        self.c.execute(sql)

        self.conn.commit()


    def empty_admin_password(self):

        ## Check Admin Table if Empty to show register page 

        rowsQuery = f"SELECT Count() FROM {self.admin_table};"
        self.c.execute(rowsQuery)
        numberOfRows = self.c.fetchone()[0]


        if (numberOfRows==0):
            return True
        else:
            return False


