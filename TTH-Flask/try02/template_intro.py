from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<user_name>")
def index(user_name='Borbuth'):
    return render_template("Borbuth.html", passed_variable=user_name)


app.run(debug=True, port=8000, host='0.0.0.0')
