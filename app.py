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
            if bcrypt.check_password_hash(user.password , password):
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
    
    if request.method == 'POST':
        print(dict(request.form))
        return redirect(url_for('home'))

    return render_template("levels.html" , questions = load_questions(sub,level) , subject = sub.capitalize() , level = level)

@app.route("/account")
def account():
    return render_template("account.html" )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home" ))

if __name__ == '__main__':
    app.run(debug = True)




