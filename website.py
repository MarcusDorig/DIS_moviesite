from flask import Flask
from flask.templating import render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("layout.html")

