from flask import render_template

from . import app
from . import models


@app.route("/")
def homepages():
    return render_template("home.html")


@app.route("/<hackathon_number>")
def hackathon(hackathon_number):
    return render_template(
    	"hackathon.html",
    	hackathon=models.Hackathon.query.filter(
            models.Hackathon.number == int(hackathon_number)
    	).one()
    )


@app.route("/project/<project_name>")
def project_page(project_name):
    return render_template(
    	"project.html",
    	project=models.Hackathon.query.filter(
            models.Project.name == project_name
        ).one()
    )


if __name__ == "__main__":
    app.run()
