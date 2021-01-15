import psycopg2
from config import config

def create_tables():
    commands = """CREATE TABLE USERS (
                                USER_ID SERIAL PRIMARY KEY,
                                NAME VARCHAR(80) NOT NULL,
                                SURNAME VARCHAR(80) NOT NULL,
                                USERNAME VARCHAR(80) NOT NULL,
                                EMAIL VARCHAR(80) NOT NULL,
                                PASSWORD VARCHAR(200) NOT NULL
                                )"""
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
    create_tables()