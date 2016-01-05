from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('template.html')


@app.route('/my-link/')
def my_link():
    print 'I got clicked!'

    return 'Click.'


@app.route('/another-link/')
def another_link():
    print 'Now i got it all'
    i = 1
    if i == 1:
        print("here i can perform a more complex logic ")
        for element in range(0, 100):
            element += 1
            print(element)
            return "this is  {}".format(element)


if __name__ == '__main__':
    app.run(debug=True)
