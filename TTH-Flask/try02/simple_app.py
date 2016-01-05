from flask import Flask

app = Flask(__name__)


# to make function a VIEW - give it a route
# decorator is a function that wraps another function e.g take index function and
# register it with our app , sd the route to "/"
@app.route("/")
def index():
    return "Fuck You!"


# defining routes should be done before app.run
app.run(debug=True, port=8000, host='0.0.0.0')
