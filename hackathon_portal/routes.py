from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename

from . import app
from . import models
from . import logic


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

def _upload_photo(file, filename):
    filename = secure_filename(file.filename)
    name, extension = filename.rsplit('.', 1)
    return logic.save_photo(file, name, extension)


@app.route("/upload_image/", methods=["POST"])
def upload_photo():
    _upload_photo(request.files['file'])
    return redirect(_upload_photo(request.files['file']))


@app.route("/upload_image_for_project/", methods=["POST"])
def upload_photo_for_project():
    photo_model = _upload_photo(request.files['file'])
    logic.associate_photo_with_project(
    	photo_model,
    	int(request.args['project_id'])
    )


if __name__ == "__main__":
    app.run()
