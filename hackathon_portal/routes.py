import os

from flask import render_template, request

from . import app


@app.route("/hello_world/")
def browse_games():
	return "Hello World."



if __name__ == "__main__":
	app.run()
