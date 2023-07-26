#!/usr/bin/python3

"""
    Starts web application listening on 0.0.0.0, port 5000
    routes:
        /states_list: list of all states in storage models
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
        Displays page with all State objects sorted by name(ASC)
    """
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """
        Removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
