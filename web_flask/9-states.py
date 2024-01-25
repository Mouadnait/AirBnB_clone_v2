#!/usr/bin/python3
"""a script that starts a flask application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_page():
    """returns a list of states"""
    states = storage.all('State').values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_with_id_page(id):
    """returns a list of states with a specific id"""
    states = storage.all('State').values()
    for state in states:
        if state.id == id:
            return render_template('9-states.html', state_id=state)
    return render_template('9-states.html')


@app.teardown_appcontext
def close_database(arg):
    """closes the current database"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
