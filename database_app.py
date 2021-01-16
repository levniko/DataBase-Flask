import psycopg2 as dbapi2
from user import User
class store():
    def add_user(conf, users):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query2 = """INSERT INTO USERS (NAME, SURNAME, USERNAME, EMAIL, PASSWORD ) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query2, (users.name, users.surname, users.username, users.email, users.password))
            connection.commit()

    def get_user(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (name, surname, nickname, email, password) = row
                return User(name, surname, nickname, email, password)
                
    def update_password(conf, username, new_password):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE USERS SET PASSWORD = %s WHERE (NICKNAME = %s)"
            cursor.execute(query, (new_password, username))
            connection.commit()    
            
    def is_exist(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (hashed,) = row
                return hashed