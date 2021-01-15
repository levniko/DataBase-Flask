import psycopg2 as dbapi2
import os
import sys
from user import User
class Recipe():
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

    # def add_resipe(self, conf, recipes):
    #     with dbapi2.connect(conf) as connection:
    #         cursor = connection.cursor()
    #         query = """INSERT INTO RECIPES (NAME, CONTENT, PHOTO) VALUES (%s, %s, %s)"""
    #         cursor.execute(query,())        