from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource,Api

#App
app = Flask(__name__)

#SqlAlchemy Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
#API calls
# api = Api(app)
# app.app_context().push()

#Creating model tables
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    
# To Define Decks Schema

#Login
@app.route('/',methods=['GET','POST'])
def loginpage():
    if request.method=='GET':
        return render_template('loginpage.html')
    elif request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        validlogin=db.session.query(User).filter(User.username==username, User.password==password).first()
        if validlogin:
            return redirect('/home'.format(username))
        return render_template('invalidpassword.html')

#Sign-up page
@app.route('/signup',methods=['GET','POST'])
def signinpage():
    if request.method=='GET':
        return render_template('signuppage.html')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        userexists=db.session.query(User).filter(User.username==username).first()
        if userexists:
            return render_template('invalid_username.html')
        user=User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

#Home page
@app.route('/home',methods=['GET'])
def Flashcard():
    return render_template("home.html")

#Run app
if __name__ == "__main__":
    app.run()
