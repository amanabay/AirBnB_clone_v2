#!/usr/bin/python3
"""
    Starts web application listening on 0.0.0.0, port 5000
    routes:
        /hbnb_filters: displays 10-hbnb_filters page
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    states = storage.all("State")
    amenities = storage.all("Amenity")

    return render_template("10-hbnb_filters.html",
                           states=states,
                           amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """
        Removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
