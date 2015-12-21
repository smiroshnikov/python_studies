from flask import Flask
from flask import request  # this is a global object

# teamtreehouse Flask basics

app = Flask(__name__)  # smart redirection to myself ?


@app.route("/")  # decorator definition from treehouse first lesson
# views can have more than 1 route - this is so fucking cool !!!
# multiple routes will make function respond to multiple end points
@app.route('/<name>')  # I don't want to use /?name=Momo anymore , its also not secure
def index(name='SecurityDAM'):
    return "{} Welcome to SDCC deployment page".format(name)


@app.route('/add/<int:num1>/<int:num2>')
# lets make our add to accept any numeric format , negatives don't work!
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
def add(num1, num2):
    return 'The sum of {} + {} = {}'.format(num1, num2, num1 + num2)


#    return '{} + {} = {}'.format(num1,num2,(int(num1)+int(num2))) # this is messy , lets cast in url!!

@app.route('/multiply/<int:num1>/<int:num2>')
def multiply(num1=5, num2=5):
    return str(num1 * num2)


# region OLD functions , that I have rewritten
"""
def old_index(name='SecurityDAM'):  # this is index view  (MCV)
    name = request.args.get('name', name)  # this is OR , either passed in srt or name variable
    return "Welcome to {} deployment page".format(name) # to pass in query use "?name=Adrian" after /
"""

app.run(host='0.0.0.0', port=4000, debug=True)
