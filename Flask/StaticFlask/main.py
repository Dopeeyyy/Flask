from flask import Flask, render_template
from admin.blueprint import blueprint
app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix="/admin")


@app.route("/")
def test():
    return "<h2>Testing the code</h2>"

if __name__ == "__main__":
    app.run(debug=True)