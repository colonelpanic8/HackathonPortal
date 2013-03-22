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
    	).one(),
    )


@app.route("/project/<project_id>")
def project_page(project_id):
    return render_template(
    	"project.html",
    	project=models.Project.query.filter(
            models.Project.id == project_id
        ).one()
    )

@app.route("/project/<project_id>/edit")
def edit_project(project_id):
    return render_template(
    	"edit_project.html",
    	project=models.Project.query.filter(
            models.Project.id == project_id
        ).one()
    )

if __name__ == "__main__":
    app.run()
