import simplejson
from flask import render_template, request, redirect
from werkzeug import secure_filename

from . import app
from . import models
from . import logic


def _upload_photo(file):
    filename = secure_filename(file.filename)
    name, extension = filename.rsplit('.', 1)
    return logic.save_photo(file, name, extension)


@app.route("/")
def homepages():
    return render_template("home.html")


@app.route("/hackathon/view/<hackathon_number>")
def hackathon(hackathon_number):
    return render_template(
    	"hackathon.html",
    	hackathon=models.Hackathon.query.filter(
            models.Hackathon.number == int(hackathon_number)
    	).one(),
    )


@app.route("/project/view/<project_id>")
def project_page(project_id):
    return render_template(
    	"project.html",
    	project=models.Project.query.filter(
            models.Project.id == project_id
        ).one()
    )


@app.route("/project/update/<attribute_name>", methods=["POST"])
def update_project_attribute(attribute_name):
    project = logic.update_project_attribute(
        int(request.form['project_id']),
	attribute_name,
        request.form[attribute_name]
    )
    return redirect("/project/{project_id}".format(project_id=project.id))


@app.route("/project/add/photo", methods=["POST"])
def add_photo_to_project():
    photo_model = _upload_photo(request.files['photo'])
    project = logic.associate_photo_with_project(
    	photo_model.id,
    	int(request.form['project_id'])
    )
    return redirect("/project/{project_id}".format(project_id=project.id))


@app.route("/project/add/member", methods=["POST"])
def add_member_to_project():
    pass

@app.route("/person/get_handles_matching")
def get_handles_starting_with():
    matching_persons = logic.get_persons_with_handles_starting_with(
    	request.args.get('handle_string', '')
    )
    return simplejson.dumps([person.yelp_handle for person in matching_persons])

if __name__ == "__main__":
    app.run()
