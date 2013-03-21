import os

from flask import render_template, request
import simplejson

from . import app
from . import logic


@app.route("/hello_world/")
def browse_games():
	return "Hello World."



if __name__ == "__main__":
	app.run()
