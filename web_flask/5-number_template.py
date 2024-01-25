#!/usr/bin/python3
"""a script that starts a flask application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """display hello hbnb"""
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb_page():
    """display hbnb"""
    return 'HBNB'


@app.route("/c/<text>", strict_slashes=False)
def C_is_fun_page(text):
    """display c plus a variable"""
    newText = text.replace('_', ' ')
    return f'C {newText}'


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_page(text="is_cool"):
    """display python is fun"""
    newText = text.replace('_', ' ')
    return f'Python {newText}'


@app.route("/number/<int:n>", strict_slashes=False)
def number_page(n):
    """display a number"""
    return f'{n} is a number'


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_html_page(n):
    """display a number"""
    return render_template('5-number.html', number=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
