from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def index(name='Borbuth'):
    return "Fuck You {}!".format(name)


app.run(debug=True, port=8000, host='0.0.0.0')
