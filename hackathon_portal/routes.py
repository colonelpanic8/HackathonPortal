import simplejson
from flask import render_template, request, redirect
from werkzeug import secure_filename

from . import app
from . import logic
from . import models
from . import util


@app.route(models.Project.view_url('<project_id>'))
def project_page(project_id):
    return render_template(
        "project.html",
        project=models.Project.query.filter(
            models.Project.id == project_id
        ).one()
    )


@app.route("/hackathon/view/<hackathon_number>")
def hackathon(hackathon_number):
    return render_template(
        "hackathon.html",
        hackathon=models.Hackathon.query.filter(
            models.Hackathon.number == int(hackathon_number)
        ).one(),
    )


@app.route(models.Person.view_url('<yelp_handle>'))
def person_page(yelp_handle):
    return render_template(
        "person.html",
        person=models.Person.query.filter(
            models.Person.yelp_handle == yelp_handle
        ).one(),
    )


@app.route(models.Project.add_url, methods=['POST', 'GET'])
def add_project():
    if request.method == 'GET':
        return render_template('upload_project.html', Project=models.Project)
    else:
        return redirect(models.Project.new(**util.remap_keys(request.form, {})).url)


@app.route(models.Person.get_handles_starting_with_url)
def get_handles_starting_with():
    matching_persons = logic.get_persons_with_handles_starting_with(
        request.args.get('handle_string', '')
    )
    return simplejson.dumps([person.yelp_handle for person in matching_persons])


def _upload_photo(file):
    filename = secure_filename(file.filename)
    name, extension = filename.rsplit('.', 1)
    return logic.save_photo(file, name, extension)


@app.route(models.Project.update_url("<attribute_name>"), methods=["POST"])
def update_project_attribute(attribute_name):
    project = logic.update_project_attribute(
        int(request.form['project_id']),
    attribute_name,
        request.form[attribute_name]
    )
    return redirect(project.url)


@app.route(models.Project.add_photo_url, methods=["POST"])
def add_photo_to_project():
    photo_model = _upload_photo(request.files['photo'])
    project = logic.associate_photo_with_project_from_ids(
        photo_model.id,
        int(request.form['project_id'])
    )
    return redirect(project.url)


@app.route(models.Project.add_person_url, methods=["POST"])
def add_member_to_project():
    project = models.Project.load(int(request.form['project_id']))
    logic.add_handles_to_project(
        [request.form['person']],
        project
    )
    return redirect(project.url)


if __name__ == "__main__":
    app.run()
