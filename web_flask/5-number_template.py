#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """display "Hello HBNB!"

    Returns:
        str: text on the index page
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """display "HBNB"

    Returns:
        str: text on the page
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """display "C", followed by the value of the text variable

    Args:
        text (str): text to be served on the page

    Returns:
        str: text on the page
    """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is cool'):
    """display "Python", followed by the value of the text variable

    Args:
        text (str): text to be served on the page

    Returns:
        str: text on the page
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """display "n is a number" only if n is an integer

    Args:
        n (integer): number to be displayed on page

    Returns:
        str: text on the page
    """
    return '{:d} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    """display a HTML page only if n is an integer

    H1 tag: "Number: n" inside the tag BODY

    Args:
        n (integer): number to be displayed on page

    Returns:
        str: text on the page
    """
    return render_template('5-number.html', num=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
