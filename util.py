import argparse
import os

from hackathon_portal import models, phonebook_etl, engrec_data_etl, server_directory, logic
from hackathon_portal.testing import factories
from sanitize_yelp_handles import SanitizeYelpHandler


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
    from hackathon_portal import image_fetcher
    hackathon = models.Hackathon.query.filter(models.Hackathon.number == 9).one()
    for project in hackathon.projects:
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

        logic.associate_photo_with_model(photo, project)

def run_bootstrap():
    #reset_tables()
    #phone_book_etl = phonebook_etl.PhoneBookETL('data/phonebook.csv')
    #phone_book_etl.execute()
    #SanitizeYelpHandler()
    data_loader_etl = engrec_data_etl.EngRecDataETL('data/hackathondata.csv')
    data_loader_etl.execute()


def make_awards():
    for award_name in ['useful', 'funny', 'cool', 'unhack', 'hardcore']:
        award = models.Award.new(name=award_name)
        models.db.session.commit()
        with open(
            os.path.join(server_directory, 'data', 'awards', "%s.jpg" % award_name)
        ) as file:
            photo = logic.add_photo(
                award_name,
                file.read(),
                'jpg'
            )
            logic.associate_photo_with_model(photo, award)
        models.db.session.commit()




if __name__ == '__main__':
    run_bootstrap()
