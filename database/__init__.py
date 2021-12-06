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

        # self.clear_database()
        self.create_database()

    def create_database(self):


        sql = 'create table if not exists ' + self.survey_table + ''' 
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  firstname varchar(20) NOT NULL,
                  lastname varchar(20) NOT NULL,
                  age int NOT NULL,
                  gender int NOT NULL,
                  ethnicity int NOT NULL,
                  disbaledValue int NOT NULL,
                  enjoyedValue int NOT NULL,
                  curiousValue int NOT NULL,
                  scienceValue int NOT NULL)

        '''

        self.c.execute(sql)

        sql = 'create table if not exists ' + self.admin_table + ''' 
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  salt varchar(64) NOT NULL,  
                  key varchar(256) NOT NULL)
        '''


        self.c.execute(sql)
        self.conn.commit()



    def drop_tables(self):
        sql = 'drop table IF EXISTS ' + self.survey_table
        self.c.execute(sql)
        sql = 'drop table IF EXISTS ' + self.admin_table
        self.c.execute(sql)
        self.conn.commit()

        
    
    def remake_database(self):
        self.drop_tables()
        self.create_database()


    def clear_survey(self):
        self.c.execute('DELETE FROM '+self.survey_table)
        self.conn.commit()



    def save_survey(self, firstname, lastname, age, gender, ethnicity, disbaledValue, enjoyedValue, curiousValue, scienceValue):
        sql = 'insert into ' + self.survey_table + f'''
        (firstname, lastname, age, gender, ethnicity, disbaledValue, enjoyedValue, curiousValue, scienceValue) values ("{firstname}", "{lastname}", {age}, {gender}, {ethnicity}, {disbaledValue}, {enjoyedValue}, {curiousValue}, {scienceValue})
        
        '''
        self.c.execute(sql)
        # print('Inserted ', firstname, lastname, age, gender, ethnicity, disbaledValue, enjoyedValue, curiousValue, scienceValue)
        self.conn.commit()

    def get_all_surveys(self):
        cursor = self.c.execute(f'select * from {self.survey_table};')
        records = cursor.fetchall()
        # print("Total rows are:  ", len(records))

        return records

 

        



    def clear_admin_password(self):
        self.c.execute('DELETE FROM '+self.admin_table)
        self.conn.commit()


    def check_admin_password(self,password):
        cursor = self.c.execute(f'select * from {self.admin_table};')
        for passwd in cursor.fetchall():
            
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


            if(key==new_key):

                return True
        
        return False



    def set_admin_password(self,password):
        self.clear_admin_password()

        salt = os.urandom(32)
        

        # Remember this

        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256 
            dklen=128 # Get a 128 byte key
        )
        # print(salt)
        # print(key)


        sql = f'''
        INSERT INTO {self.admin_table} (salt,key)
VALUES ("{salt.hex()}", "{key.hex()}");
        '''
        self.c.execute(sql)

        self.conn.commit()


    def empty_admin_password(self):

        rowsQuery = f"SELECT Count() FROM {self.admin_table};"
        self.c.execute(rowsQuery)
        numberOfRows = self.c.fetchone()[0]


        if (numberOfRows==0):
            return True
        else:
            return False


