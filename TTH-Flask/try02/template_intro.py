from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<user_name>")
def index(user_name='Sergei Miroshnikov'):
    return render_template("index.html", passed_variable=user_name)


@app.route("/add/<int:A>/<int:B>")
def add(A=2, B=2):
    passed_dict = {'number1': A, 'number2': B}
    return render_template("add.html", **passed_dict)  # unpacking dictionary


app.run(debug=True, port=8000, host='0.0.0.0')
