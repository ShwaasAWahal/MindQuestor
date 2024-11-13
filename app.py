from flask import Flask , render_template , url_for , request , redirect , flash
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
    test_4_score2 = db.Column(db.Integer() ,default = None )
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))


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
            else:
                flash("Wrong Password! Try Again")
        else:
            flash("This user does not exist!")    
    return render_template('login.html')
    

@app.route("/signup" , methods = ['GET' , 'POST'])
def SignUp():
    
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
            flash("This user already exists!Please try again")
    return render_template('signup.html')

@app.route("/forgotpassword" , methods = ['GET' , 'POST'])
def forgot():
    if request.method == "POST":
        print(request.form['email'])
        user = User.query.filter_by(Email = request.form["email"]).first()
        print(user)
        if user:
            new_pass = request.form['password']
            print(new_pass)
            con_pass = request.form['con_password']
            print(con_pass)
            if new_pass == con_pass:
                user.password = bcrypt.generate_password_hash(new_pass).decode("utf-8")
                db.session.commit()
                return redirect(url_for('home'))
    return render_template("forgot.html")


@app.route("/subjects/<sub>")
def Subjects(sub):
    if sub == "math":
        fullSub = "Engineering Mathematics"
    elif sub == "physics":
        fullSub = "Electromagnetsim and Mechanics"
    elif sub == "python":
        fullSub = "Computational Thinking & Programming"
    elif sub == "java":
        fullSub = "Java"

    return render_template("subject.html" , subject = sub , fullSub = fullSub)

@app.route("/subjects/<sub>/<int:level>" , methods = ['GET' , 'POST'])
def level(sub , level):
    marks = 0
    answered_all = True
    
    questions = load_questions(sub , level)

    score = 0

    all_answers = []
    all_scores = []
    for i in questions.values():
        all_answers.append(i[4].strip())
        if level == 4:
            all_scores.append(i[5])
    
    

    print(all_answers)

    if level == 1:
        dif = "Easy"
    elif level == 2:
        dif = "Medium"
    elif level == 3:
        dif = "Hard"
    elif level == 4:
        dif = "Mixed"

    
    if request.method == 'POST':

        UserId = current_user.id
        if Result.query.filter_by(user_id = UserId , subject = sub).first():
             user = Result.query.filter_by(user_id = UserId , subject = sub).first()
        else:
            user = Result(subject = sub , user_id = UserId)
        

        values = list(dict(request.form).values())
        print(values)
        if len(values) == len(all_answers):
            for i in range(len(values)):
                answer = values[i].strip()
                correct_answer = all_answers[i].strip()
                if answer == correct_answer:
                    marks += 2
                    if level == 4:
                        score += all_scores[i]

            if level == 1:
                user.test_1_score = marks
            elif level == 2:
                user.test_2_score = marks
            elif level == 3:
                user.test_3_score = marks
            elif level == 4:
                user.test_4_score = marks
                user.test_4_score2 = score

            if not Result.query.filter_by(user_id = UserId , subject = sub).first():
                db.session.add(user)

            db.session.commit()
            print(marks)
            print(score)
            return redirect(url_for('result' , sub = sub , level = level , score = score))
        else:
            flash("Please Attempt all questions")
            answered_all = False
    print(answered_all)
    return render_template("levels.html" , questions = questions , subject = sub.capitalize() , level = dif , answered_all = answered_all)

@app.route("/account")
def account():
    UserId = current_user.id
    userPy = Result.query.filter_by(user_id = UserId , subject = "python").first()
    userPh = Result.query.filter_by(user_id = UserId , subject = "physics").first()
    userMa = Result.query.filter_by(user_id = UserId , subject = "math").first()
    userJa = Result.query.filter_by(user_id = UserId , subject = "java").first()
    print(userPy , userPh , userMa , userJa)
    return render_template("dashboard.html" , userPy = userPy , userPh = userPh , userMa = userMa , userJa = userJa)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home" ))

@app.route("/subjects/<sub>/<int:level>/result")
def result(sub , level):
    UserId = current_user.id
    user = Result.query.filter_by(user_id = UserId , subject = sub).first()
    marks = 0
    score = 0
    scoreper = 0
    if level != 4:
        if level == 1:
                marks = user.test_1_score
        elif level == 2:
                marks = user.test_2_score
        elif level == 3:
                marks = user.test_3_score
        marksper = (marks/10) * 100
        scoreper = (score / 240) * 100
    else:
        marks = user.test_4_score
        marksper = (marks/24) * 100
        score = user.test_4_score2
        scoreper = (score / 240) * 100
    

    return render_template("score.html" , marks = marks , level = level ,score = score , scoreper = scoreper , marksper = marksper)


@app.route("/error")
def error():
     return render_template("error.html")
if __name__ == '__main__':
    app.run(debug = True)




