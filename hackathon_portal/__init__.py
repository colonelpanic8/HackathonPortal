from __future__ import absolute_import
import os

from flask import Flask, url_for

application_directory = os.path.abspath(os.path.dirname(__file__))
server_directory, _ = os.path.split(application_directory)
photo_directory = os.path.join(application_directory, 'static', 'photo')

app = Flask(__name__)
app.jinja_env.globals['get_static_url'] = lambda filename: url_for('static', filename=filename)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///{app_dir}/database.db'.format(
        app_dir=server_directory
    )
)
app.debug = True
