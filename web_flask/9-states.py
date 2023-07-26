#!/usr/bin/python3
"""
    Starts web application listening on 0.0.0.0, port 5000
    routes:
        /states: lists all states
        /states/<id>: If a State object is found with <id>
        list cities in the state
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    """
        Displays all State objects sorted by name(ASC)
    """
    states = storage.all("State")
    return render_template('9-states.html', state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    states = storage.all("State")

    for state in states.values():
        if state.id == id:
            return render_template('9-states.html', state=state)

    return render_template('9-states.html')


@app.teardown_appcontext
def teardown(exc):
    """
        Removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
