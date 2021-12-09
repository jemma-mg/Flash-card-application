from enum import unique
from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy.sql import func
# from flask_restful import Resource,Api

#App
app = Flask(__name__)

#SqlAlchemy Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

#Creating model tables
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
  
class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    deckname = db.Column(db.String, nullable = False)
    # deck = db.Column(db.String, db.ForeignKey('deck.deckname'), nullable = False)
    front = db.Column(db.String)
    back = db.Column(db.String)

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
    conn=sqlite3.connect("database.sqlite3")
    cur=conn.cursor()
    query="""SELECT deckname from card WHERE front IS NULL"""
    cur.execute(query)
    rows=cur.fetchall()
    cur.close()
    return render_template("index.html",rows=rows)

#Create deck
@app.route('/createdeck',methods=['GET','POST'])
def createdeck():
    if request.method=="POST":
        deckname=request.form['deckname']
        conn=sqlite3.connect("database.sqlite3")
        cur=conn.cursor()
        query="""INSERT INTO card (deckname) VALUES (?)"""
        cur.execute(query,(deckname,))
        conn.commit()
        return redirect("/home")
    return render_template('createdeck.html')

#delete deck
@app.route('/deletedeck/<deckname>')
def deletedeck(deckname):
    conn=sqlite3.connect("database.sqlite3")
    cur=conn.cursor()
    query="""DELETE FROM card WHERE deckname=?"""
    cur.execute(query,(deckname,))
    conn.commit()
    return redirect("/home")

#update deck
@app.route('/updatedeck/<deckname>',methods=['GET','POST'])
def updatedeck(deckname):
    if request.method=="POST":
        old=deckname
        new=request.form['new']
        conn=sqlite3.connect("database.sqlite3")
        cur=conn.cursor()
        query="""UPDATE card SET deckname=? WHERE deckname=?"""
        cur.execute(query,(new,old))
        conn.commit()
        return redirect("/home")
    return render_template('updatedeck.html',deckname=deckname)


#review deck
@app.route('/review/<deckname>')
def review(deckname):
    conn=sqlite3.connect("database.sqlite3")
    cur=conn.cursor()
    query="""SELECT * FROM card WHERE deckname=? AND front IS NOT NULL ORDER BY RANDOM() LIMIT 1"""
    cur.execute(query,(deckname,))
    rows=cur.fetchone()
    if rows is not None:
        return render_template('review.html',deckname=deckname,rows=rows)
    else:
        return redirect("/home")

#Add card to deck
@app.route('/addcard/<deckname>',methods=['GET','POST'])
def addcard(deckname):
    if request.method=="POST":
        front=request.form['front']
        back=request.form['back']
        conn=sqlite3.connect("database.sqlite3")
        cur=conn.cursor()
        query="""INSERT INTO card (deckname,front,back) VALUES (?,?,?)"""
        cur.execute(query,(deckname,front,back))
        conn.commit()
        return redirect("/home")
    return render_template('addcard.html',deckname=deckname)

#Run app
if __name__ == "__main__":
    app.run(debug=True)
