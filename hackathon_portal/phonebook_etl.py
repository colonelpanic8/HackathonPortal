import etl
import logic


FIRST_NAME = "First"
LAST_NAME = "Last"
EMAIL = "Email"

class PhoneBookTransformer(etl.Transformer):

	def transform(self, raw_data):
		return raw_data


class PhoneBookLoader(etl.Loader):
	def load(self, phonebook):
		persons = []
		for entry in phonebook:
			person = {
				'name': ' '.join([
					entry[FIRST_NAME],
					entry[LAST_NAME]
				]),
				'yelp_handle': entry[EMAIL]
			}
			persons.append(person)

		logic.add_persons(persons)


class PhoneBookETL(etl.ETL):

	extractor = etl.CSVExtractor()

	transformers = [
		PhoneBookTransformer()
	]

	loader = PhoneBookLoader()

	def transform(self):
		current_data = self.raw_data
		for transformer in self.transformers:
			current_data = transformer.transform(current_data)

		self.transformed = current_data