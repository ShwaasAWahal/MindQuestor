from flask import Flask, render_template, redirect, request, session
##MySQL Connection
'''
def connect(con , cursor):
    con=c.connect (host="localhost",user="root", passwd="shoyshwaas")
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
    con.commit()'''

