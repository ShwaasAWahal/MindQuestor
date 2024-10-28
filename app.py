from flask import Flask , render_template , url_for , request
import mysql.connector

app = Flask("__name__")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register" , methods=['POST' , 'GET'])
def register():
    if request.method == 'POST':
        print(dict(request.form)["em"])
    return render_template('register.html')


@app.route("/login" , methods = ['GET' ,'POST'])
def login():
    return "<h1> Hello World! </h1>"





if __name__ == '__main__':
    app.run(debug = True)