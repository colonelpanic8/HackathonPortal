from flask import render_template, request

from . import app


@app.route("/")
def homepages():
    return render_template("home.html")

@app.route("/project/<project_name>")
def project_page(project_name):
    return render_template("project.html", project_name=project_name)



if __name__ == "__main__":
	app.run()
