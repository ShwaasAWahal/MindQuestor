from flask import Flask , render_template , url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.app_context().push()
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String(255) ,nullable = False )
    Email = db.Column(db.String(255) ,nullable = False )
    password = db.Column(db.String(255) ,nullable = False )
    results = db.relationship('Result' , backref = 'user')

    def __repr__(self):
        return f"{self.Email}"

class Result(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    subject = db.Column(db.String(255) ,nullable = False )
    test_1_score = db.Column(db.Integer() ,default = None )
    test_2_score = db.Column(db.Integer() ,default = None )
    test_3_score = db.Column(db.Integer() ,default = None )
    test_4_score = db.Column(db.Integer() ,default = None )
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    

questions = {"What is 1 + 1" : [1 ,2 ,3 ,4] , "What is 2+2" : [3 , 5 , 6 , 8] , "what is 3 + 3" : [2 , 3 , 4 , 6]}

@app.route("/")
@app.route("/home" , methods = ['GET' , 'POST'])
def home():
    subject = ""
    return render_template('main_web_page.html' , sub = subject)


@app.route("/signin" , methods = ['POST' , 'GET'])
def SignIn():
    if request.method == 'POST':
        ''' 
    already_exists = True
        auth = False
        if request.method == 'POST':
            user = User.query.filter_by(user_name = request.form['email']).first()
            if request.form['email'] in User.query.all():
                already_exists = True
                email = user.Email
                password = user.password
                if password == request.form['password']:
                    auth = True
        print("User Exists: " , already_exists)
        print("Password?: " , auth)
        '''
        pass
    return render_template('signin.html')

@app.route("/signup" , methods = ['GET' , 'POST'])
def SignUp():
    already_exists = False
    if request.method == 'POST':
        if not User.query.filter_by(Email = request.form['email']).first():
            user = User(
                user_name = request.form['username'] ,
                Email = request.form['email'] ,
                password = request.form['password']
                )
            db.session.add(user)
            db.session.commit()
            print(User.query.filter_by(Email = request.form['email']).first())
        else:
            already_exists = True
        print(already_exists)
    return render_template('signup.html' , exists = already_exists)


@app.route("/subjects/<sub>")
def Subjects(sub):
    return render_template("subject.html" , subject = sub , subC = sub.capitalize())

@app.route("/subjects/<sub>/<level>" , methods = ['GET' , 'POST'])
def level(sub , level):
    if request.method == 'POST':
        for i in request.form:
            print(request.form[i])
    return render_template("levels.html" , questions = questions , subject = sub.capitalize() , level = level)



if __name__ == '__main__':
    app.run(debug = True)




