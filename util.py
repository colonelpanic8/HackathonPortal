import argparse
from hackathon_portal import models
from hackathon_portal.testing import factories


def parse_host_and_port():
	parser = argparse.ArgumentParser()
	parser.add_argument(
            '--port',
            action='store',
            type=int,
            dest='port',
            default=5000,
            help='The port that should be listned on.',
	)
	parser.add_argument(
            '--host',
            action='store',
            type=str,
            dest='host',
            default='0.0.0.0',
            help='The IP address on which to run the server.'
	)
	namespace = parser.parse_args()
	return namespace.host, namespace.port


def reset_tables():
	models.db.drop_all()
	models.db.create_all()


def reset_tables_and_build_hackathon_fixtures():
    reset_tables()
    for i in range(10):
        factories.build_hackathon_fixture(i)


def fill_projects_with_default_photos():
    from hackathon_portal import image_fetcher, logic
    for project in models.Project.query.all():
        if project.photos:
            continue
	for project in models.Hackathon.query.filter(models.Hackathon.number == 7).one().projects:
            if project.photos:
                continue
            image_url = image_fetcher.ImageFetcher(project.name).get_my_image()
            _, extension = image_url.rsplit('.', 1)
            photo = logic.add_photo(
                project.name,
                logic.download_image_from_url(image_url),
                extension
            )

        logic.associate_photo_with_project(photo, project)


if __name__ == '__main__':
    reset_tables()
