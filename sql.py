import mysql.connector as c
from flask import Flask, render_template, redirect, request, session
##MySQL Connection
con=c.connect (host="localhost",user="root", passwd="Yash@12345")
cursor=con.cursor()
cursor.execute("create database if not exists MindQuestor_db")
cursor.execute("use MindQuestor_db")

##Creating Required Tables
cursor.execute("""create table if not exists user_details(
               ID int auto_increment primary key, 
               USER_NAME varchar(255) not null,
               EMAIL varchar(255) not null,
               PASSWORD varchar(255) not null )""")
cursor.execute("""create table if not exists results(
               ID int auto_increment primary key,
               USER_ID int,
               SUBJECT varchar(255),
               Test_1_Score int default NULL,
               Test_2_Score int default NULL,
               Test_3_Score int default NULL,
               Test_4_Score int default NULL,
               FOREIGN KEY (USER_ID) REFERENCES user_details(ID))""")
con.commit()

##Route for Signup
@app.route("/")
@app.route("/signup", methods = ["Get", "Post"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor.execute("INSERT INTO user_details (user_name, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        db.commit()

        session['username'] = username
        return redirect('/subjects')

    return render_template('signup.html')

