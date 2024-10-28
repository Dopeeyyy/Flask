from flask import Flask, render_template, url_for, request, redirect, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "y"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

database = SQLAlchemy(app)

class User(database.Model):
    _id = database.Column("id", database.Integer, primary_key=True)
    name = database.Column("name", database.String(50), unique=True)
    email = database.Column("email", database.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values=User.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        
        found_user = User.query.filter_by(name=user).delete()
        for user in found_user:
            user.delete()
        if found_user:
            session["user"] = found_user.name
            session["email"] = found_user.email
            flash("Log-in successfully!", "info")
            return redirect(url_for("user"))
        else:
            usr = User(user, None)
            database.session.add(usr)
            database.session.commit()  
            flash("User created and logged in!", "info")
            return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"You've already logged in as {session['user']}!", "info")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        found_user = User.query.filter_by(name=user).first()
        
        email = found_user.email
        name = found_user.name

        if request.method == "POST":
            email = request.form["email"]
            found_user.email = email
            database.session.commit()
            flash("Profile updated successfully!", "info")

        return render_template("user.html", email=email, name=name, user=user)

    flash("You are not logged in!", "info")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You've successfully logged out, {user}.", "info")
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    with app.app_context():
        database.create_all()
        print("Database tables created successfully.")
    app.run(debug=True)
