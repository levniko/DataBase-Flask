import psycopg2 
from flask import Flask, render_template, url_for,request,redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from user import User
from config import config	
from database_app import Recipe
import psycopg2 as dbapi2
from database_app import Recipe
import hashlib # included in Python library, no need to install
app = Flask(__name__)

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

lm=LoginManager()


@app.route("/")
def home_page():
	return render_template("home.html")

@app.route("/search")
def search_page():
    return render_template("search.html")

@app.route("/add")
def add_page():
    return render_template("add_recipe.html")

@app.route("/myaccount")
def account_page():
    return render_template("account.html")
    
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    # username = request.form['username']
    # password = request.form['password']
    # truepassword = Recipe.is_exist(app.config['dsn'], username)
    # if truepassword:
    #     user = Recipe.get_user(app.config['dsn'], username)
    #     if pwd_context.verify(password, truepassword):
    #         login_user(user)
    #         return redirect(url_for('home_page'))
    #     else:
    #         return redirect(url_for('login'))

    # else:
    #     return redirect(url_for('login'))


@app.route("/register",methods=['GET','POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')

    user = User(request.form['name'], request.form['surname'], request.form['username'], request.form['password'], request.form['email'])
    print(user.name)
    # if Recipe.is_exist(request.form['nickname']):
    #     return render_template('register.html', error = "This username is already taken.")
    Recipe.add_user(user)
    return redirect(url_for('login_page'))

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect() as connection:
        db_cursor = connection.cursor()
        query =     """CREATE TABLE USERS (
                        USER_ID SERIAL PRIMARY KEY,
                        NAME VARCHAR(80) NOT NULL,
                        SURNAME VARCHAR(80) NOT NULL,
                        USERNAME VARCHAR(80) NOT NULL,
                        EMAIL VARCHAR(80) NOT NULL,
                        PASSWORD VARCHAR(200) NOT NULL
                        )"""

        db_cursor.execute(query)

if __name__ =="__main__":

    connect()
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)
