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
    print os.popen('ls -la')
    return "fuck!"


if __name__ == '__main__':
    app.run(debug=True)
