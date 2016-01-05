from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def index(name='Borbuth'):
    return render_template("Borbuth.html")


app.run(debug=True, port=8000, host='0.0.0.0')
