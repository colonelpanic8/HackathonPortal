from flask import render_template

from . import app


@app.route("/")
def homepages():
    return render_template("home.html")

@app.route("/<hackathon_id>")
def hackathon(hackathon_id):
    project_list = [
        {
             'name': 'Project1',
             'description': 'This is project 1',
             'members': ['jchuah','chao','imalison']
	},
        {
             'name': 'Project2',
             'description': 'This is project 2',
             'members': ['sri', 'jkotker']
        },
        {
             'name': 'Project2',
             'description': 'This is project 2',
             'members': ['sri', 'jkotker']
        }
    ]
    return render_template("hackathon.html", hackathon_id=hackathon_id, project_list=project_list)

@app.route("/project/<project_name>")
def project_page(project_name):
    return render_template("project.html", project_name=project_name)


if __name__ == "__main__":
	app.run()
