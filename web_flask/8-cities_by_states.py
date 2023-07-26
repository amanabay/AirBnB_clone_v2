#!/usr/bin/python3

"""
    Starts web application listening on 0.0.0.0, port 5000
    routes:
        /cities_by_states: lists cities found in states
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
        Displays cities in states
    """
    states = storage.all("State")
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """
        Removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
