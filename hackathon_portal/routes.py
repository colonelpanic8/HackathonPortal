from flask import render_template, request, redirect
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


@app.route("/update_project/<attribute_name>", methods=["POST"])
def update_project_attribute(attribute_name):
    project = logic.update_project_attribute(
        int(request.form['project_id']),
	attribute_name,
        request.form[attribute_name]
    )
    return redirect("/project/{project_id}".format(project_id=project.id))


def _upload_photo(file):
    filename = secure_filename(file.filename)
    name, extension = filename.rsplit('.', 1)
    return logic.save_photo(file, name, extension)


@app.route("/upload_image/", methods=["POST"])
def upload_photo():
    _upload_photo(request.files['file'])
    return redirect(_upload_photo(request.files['file']))


@app.route("/upload_photo_for_project/", methods=["POST"])
def upload_photo_for_project():
    photo_model = _upload_photo(request.files['photo'])
    project = logic.associate_photo_with_project(
    	photo_model.id,
    	int(request.form['project_id'])
    )
    return redirect("/project/{project_id}".format(project_id=project.id))

if __name__ == "__main__":
    app.run()
