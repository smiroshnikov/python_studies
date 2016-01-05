from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")  # better way to pass arguments
def index(name='Borbuth'):
    return "Fuck You {}!".format(name)


@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<int:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<float:num2>')
def add(num1, num2):
    return "{}+{}={}".format(num1, num2, str(num1 + num2))


app.run(debug=True, port=8000, host='0.0.0.0')
