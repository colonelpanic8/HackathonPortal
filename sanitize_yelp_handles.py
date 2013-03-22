from hackathon_portal import logic


class SanitizeYelpHandler(object):

    def __init__(self):
        persons = logic.get_all_persons()
        for person in persons:
            at_location = person.yelp_handle.find('@')
            if at_location >= 0:
                person.yelp_handle = person.yelp_handle[:at_location]
        logic.models.db.session.commit()


if __name__ == '__main__':
	SanitizeYelpHandler()
