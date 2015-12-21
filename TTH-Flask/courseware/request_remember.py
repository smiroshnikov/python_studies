from flask import Flask
from flask import request

app = Flask(__name__)


# query string look like this /?name=Fuck!

@app.route('/')
@app.route('/<name>')
def index(name="Momo"):
    return "hey ! {}".format(request.args.get('name', name))


@app.route('/multiply')
@app.route('/multiply/<int:num1>/<int:num2>')
def multiply(num1=5, num2=5):
    result = num1 * num2
    return str(result)


app.run(host='0.0.0.0', port=4000, debug=True)
