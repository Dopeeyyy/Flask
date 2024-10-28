from flask import Flask, render_template, url_for, request, redirect, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key = "y" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

database= SQLAlchemy(app)

class users(database.Model):
    _id = database.Column("id", database.Integer, primary_key=True)
    user = database.Column("user",database.String(25)) 
    name = database.Column("name",database.String(50))
    password = database.Column("password",database.String(50))
    email = database.Column("email",database.String(100))

    def __init__(self, user, name, email, password,):
        self.name = name
        self.email = email
        self.password = password
        self.user = user

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        #session.permanent= True (If I wanna make the data I type last forever)
        user = request.form["username"]
        session["user"]= user
        password = request.form["password"]
        session["password"]= password
        flash(f"You've been successfully log-in successful, congrats {user}!", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"You've already logged in as {session['user']}!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST","GET"])
def user():
    email= None
    name= None
    if "user" in session and "password" in session:
        user = session["user"]
        password = session["password"]

        if request.method == "POST":
            email = request.form["email"]
            name = request.form["name"]
            user = session["user"]
            session["name"] = name
            session["email"] = email
        else:
            if "email" in session and "name" in session:
                user = session["user"]
                name = session["name"]
                email = session["email"]

        return render_template("user.html", email=email, name=name, user=user)
    else:
        flash(f"You are not log-in {user}!", "info")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    if "user" in session and "password" in session:
        user = session["user"]
        flash(f"You've been successfully logout, congrats {user}!", "info")
    session.pop("user", None)
    session.pop("password", None)
    session.pop("name", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    database.create_all()
    app.run(debug=True)
