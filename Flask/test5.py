from flask import Flask, render_template, url_for, request, redirect, session
from datetime import timedelta
app = Flask(__name__)

app.secret_key = "y" 
app.permanent_session_lifetime = timedelta(minutes=10)

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
        return redirect(url_for("user"))
    else:
        if "user" in session and "password" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session and "password" in session:
        user = session["user"]
        password = session["password"]
        return f"<h2>Hello {user}, remember your password is {password}</h2>"
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("password", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
