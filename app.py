from flask import Flask , render_template , url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.app_context().push()
class Database(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String(255) ,nullable = False )
    Email = db.Column(db.String(255) ,nullable = False )
    password = db.Column(db.String(255) ,nullable = False )

    def __repr__(self):
        return f"{self.id} - {self.Email} - {self.user_name}"
    

questions = {"What is 1 + 1" : [1 ,2 ,3 ,4] , "What is 2+2" : [3 , 5 , 6 , 8] , "what is 3 + 3" : [2 , 3 , 4 , 6]}

@app.route("/")
@app.route("/home" , methods = ['GET' , 'POST'])
def home():
    subject = ""
    return render_template('main_web_page.html' , sub = subject)


@app.route("/signin" , methods = ['POST' , 'GET'])
def SignIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    return render_template('signin.html')

@app.route("/signup" , methods = ['GET' , 'POST'])
def SignUp():
    if request.method == 'POST':
        print(request.form)
    return render_template('signup.html')


@app.route("/subjects/<sub>")
def Subjects(sub):
    return render_template("subject.html" , subject = sub , subC = sub.capitalize())

@app.route("/subjects/<sub>/<level>" , methods = ['GET' , 'POST'])
def level(sub , level):
    if request.method == 'POST':
        for i in request.form:
            print(request.form[i])
        #print(request.form)
    return render_template("levels.html" , questions = questions , subject = sub.capitalize() , level = level)



if __name__ == '__main__':
    app.run(debug = True)