from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("user", usr=user, pwd=password))

    else:
        return render_template("login.html")


@app.route("/<usr>/<pwd>")
def user(usr, pwd):
    return f"<h2>Hello {usr}!</h2><h3>Your password is {pwd}, make sure your alone</h2>"

if __name__ == '__main__':
    app.run(debug=True)
