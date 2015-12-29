from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/multiply')
@app.route('/multiply/<int:num1>/<int:num2>')
@app.route('/multiply/<float:num1>/<int:num2>')
@app.route('/multiply/<int:num1>/<float:num2>')
@app.route('/multiply/<float:num1>/<float:num2>')
def multiply(num1=5, num2=5):
    # product = num1 * num2
    context = {'num1': num1, 'num2': num2}
    # return str(product)
    return render_template("multiply.html", **context)


@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<int:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<float:num2>')
def add(num1, num2):
    context = {'num1': num1, 'num2': num2}
    return render_template("add.html", **context)


@app.route("/")
@app.route("/<name>")
def index(name='Developer'):
    context = {'name': name}
    return render_template("index.html", **context)

app.run(host='0.0.0.0', port=4000, debug=True)
