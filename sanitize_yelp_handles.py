from hackathon_portal import logic
from hackathon_portal import models

class SanitizeYelpHandler(object):

	def __init__(self):
		persons = logic.get_all_persons()
		for person in persons:
			person.yelp_handle = person.yelp_handle[
				:person.yelp_handle.find('@')
			]


if __name__ == '__main__':
	SanitizeYelpHandler()
