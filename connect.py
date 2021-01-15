#!/usr/bin/python
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users (
                        user_id SERIAL PRIMARY KEY,
                        name VARCHAR(80) NOT NULL,
                        surname VARCHAR(80) NOT NULL,
                        username VARCHAR(80) NOT NULL,
                        email VARCHAR(80) NOT NULL,
                        password VARCHAR(200) NOT NULL
                        )
                        """
                        )

    # commands = """CREATE TABLE USERS (
    #                             USER_ID SERIAL PRIMARY KEY,
    #                             NAME VARCHAR(80) NOT NULL,
    #                             SURNAME VARCHAR(80) NOT NULL,
    #                             USERNAME VARCHAR(80) NOT NULL,
    #                             EMAIL VARCHAR(80) NOT NULL,
    #                             PASSWORD VARCHAR(200) NOT NULL
    #                             )"""
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    connect()
    create_tables()