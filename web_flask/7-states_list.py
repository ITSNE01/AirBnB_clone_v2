#!/usr/bin/python3
""" A script that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ States list page """
    all_states = list(storage.all(State).values())
    all_states.sort(key=lambda x: x.name)
    return render_template('7-states_list.html', states=all_states)


@app.teardown_appcontext
def flask_teardown(exc):
    """ Close the current SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
