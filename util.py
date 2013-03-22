import argparse


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


def reset_tables_and_build_hackathon_fixtures():
    from hackathon_portal import models
    from hackathon_portal.testing import factories
    models.db.drop_all()
    models.db.create_all()
    for i in range(10):
        factories.build_hackathon_fixture(i)


if __name__ == '__main__':
    reset_tables_and_build_hackathon_fixtures()
