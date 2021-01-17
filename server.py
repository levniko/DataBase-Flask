import psycopg2 
from flask import Flask, render_template, url_for,request,redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from user import User
from config import config	
from database_app import store
import psycopg2 as dbapi2
import hashlib 
from passlib.apps import custom_app_context as pwd_context
import datetime
import json
import os
import psycopg2 as dbapi2
import re

app = Flask(__name__)
conn = psycopg2.connect(database="recipe", user = "postgres", password = "1573596248", host = "127.0.0.1", port = "5432")


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

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
    username = request.form['username']
    password = request.form['password']
    truepassword = store.is_exist(username)
    if truepassword:
        user = store.get_user(username)
        if pwd_context.verify(password, truepassword):
            login_user(user)
            return redirect(url_for('home_page'))
        else:
            return redirect(url_for('login_page'))

    else:
        return redirect(url_for('login_page'))

@app.route("/register",methods=['GET','POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        user = User(request.form['name'], request.form['surname'], request.form['username'], request.form['password'], request.form['email'])
        # if store.is_exist(app.config['dsn'], request.form['username']):
        #     return render_template('register.html', error = "This username is already taken.")
        store.add_user(user)
        return redirect(url_for('login_page'))

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERS CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE USERS (
                                 USER_ID SERIAL PRIMARY KEY,
                                 NAME VARCHAR(80) NOT NULL,
                                 SURNAME VARCHAR(80) NOT NULL,
                                 USERNAME VARCHAR(80) NOT NULL,
                                 EMAIL VARCHAR(80) NOT NULL,
                                 PASSWORD VARCHAR(200) NOT NULL
                                 )"""
        cursor.execute(query)
        connection.commit()

    return redirect(url_for('home_page'))

if __name__ =="__main__":

    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)
