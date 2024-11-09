from flask import Flask , render_template , url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import   LoginManager, login_user , current_user , UserMixin , logout_user
from filehandling import load_questions



app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '86259b855ea5dfb53e9e809e6d8dbe7f'

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


app.app_context().push()
class User(db.Model , UserMixin):
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
    return render_template('main_web_page.html' )


@app.route("/login" , methods = ['POST' , 'GET'])
def LogIn():
    if request.method == 'POST':
        user = User.query.filter_by(Email = request.form['email']).first()
        if user != None:
            password = request.form['password']
            if bcrypt.check_password_hash(user.password , password ):
                login_user(user)
                return redirect(url_for("home" ))    
    return render_template('login.html')

@app.route("/signup" , methods = ['GET' , 'POST'])
def SignUp():
    
    already_exists = False
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = User.query.filter_by(Email = request.form['email']).first()
        if not user:
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode("utf-8")
            user = User(
                user_name = request.form['username'] ,
                Email = request.form['email'] ,
                password = hashed_password
                )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('LogIn'))
        else:
            already_exists = True
    return render_template('signup.html' , exists = already_exists)


@app.route("/subjects/<sub>")
def Subjects(sub):
    
    return render_template("subject.html" , subject = sub)

@app.route("/subjects/<sub>/<int:level>" , methods = ['GET' , 'POST'])
def level(sub , level):
    marks = 0
    questions = load_questions(sub , level)
    print(questions.values())
    if request.method == 'POST':

        UserId = current_user.id
        if Result.query.filter_by(user_id = UserId).first():
             user = Result.query.filter_by(id = UserId).first()
        else:
            user = Result(subject = sub , user_id = UserId)

        j = 0
        for i in questions:
            correct_answer = questions[i][4].strip()
            print(correct_answer)
            answer = list(dict(request.form).values())[j].strip()
            j += 1
            
            if answer == correct_answer:
                marks += 1


        if level == 1:
            user.test_1_score = marks
        elif level == 2:
            user.test_2_score = marks
        elif level == 3:
            user.test_3_score = marks
        elif level == 4:
            user.test_4_score = marks
    
        db.session.add(user)
        db.session.commit()
        print(marks)
        return redirect(url_for('result' , sub = sub , level = level))
    return render_template("levels.html" , questions = questions , subject = sub.capitalize() , level = level)

@app.route("/account")
def account():
    UserId = current_user.id
    user = Result.query.filter_by(user_id = UserId).first()
    return render_template("dashboard.html" , user = user )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home" ))

@app.route("/subjects/<sub>/<int:level>/result")
def result(sub , level):
    UserId = current_user.id
    user = Result.query.filter_by(user_id = UserId).first()
    marks = None
    if level == 1:
            marks = user.test_1_score
    elif level == 2:
            marks = user.test_2_score
    elif level == 3:
            marks = user.test_3_score
    elif level == 4:
            marks = user.test_4_score

    return render_template("score.html" , marks = marks * 2)

if __name__ == '__main__':
    app.run(debug = True)




