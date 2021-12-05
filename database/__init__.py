import sqlite3

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
                  first_name varchar(20) NOT NULL,
                  last_name varchar(20) NOT NULL)

        '''

        self.c.execute(sql)

        sql = 'create table if not exists ' + self.admin_table + ''' 
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  password varchar(20) NOT NULL)
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


    def insert_survey(self, id):
        sql = 'insert into ' + self.survey_table + ' (id) values (%d)' % (id)
        self.c.execute(sql)
        print('Inserted ', id)
        self.conn.commit()


    def clear_admin_password(self):
        self.c.execute('DELETE FROM '+self.admin_table)
        self.conn.commit()



    def check_admin_password(self,password):
        cursor = self.c.execute(f'select * from {self.admin_table};')
        for passwd in cursor.fetchall():
            if(passwd[1]==password):
                return True
        
        return False



    def set_admin_password(self,password):
        self.clear_admin_password()
        sql = f'''
        INSERT INTO {self.admin_table} (password)
VALUES ("{password}");
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


