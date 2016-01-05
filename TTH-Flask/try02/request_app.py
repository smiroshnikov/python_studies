from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def index(name='Borbuth'):
    name = request.args.get('name', name)  # ?name=Bob [not used]
    return "Fuck You {}!".format(name)


app.run(debug=True, port=8000, host='0.0.0.0')
