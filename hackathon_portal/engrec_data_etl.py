import etl
import util


class EngRecDataTransformer(etl.Transformer):

	HACKATHON_ID = 'HackathonID'
	PROJECT_MEMBERS = "ProjectMembers"

	external_to_internal_field_names_map = {
		"Project Name": "ProjectName",
		"ALL People on Your Team": PROJECT_MEMBERS,
		"What's your project about? Give us some deets! ": "ProjectDetails"
	}

class EngRecDataHackathonTransformer(EngRecDataTransformer):


	def transform(self, raw_data):
		current_hackathon_id = None
		data_with_hackathon_details = []
		for row in raw_data:
			if 'H@ckathon' in row['Timestamp']:
				raw_hackathon_id = row['Timestamp']
				current_hackathon_id = raw_hackathon_id[:raw_hackathon_id.find(' Below')]
			else:
				row[self.HACKATHON_ID] = current_hackathon_id
				data_with_hackathon_details.append(row)

		return data_with_hackathon_details


class EngRecDataProjectMemberTransformer(EngRecDataTransformer):

	def __init__(self):
		self.name_parser = util.NameParser()

	def transform(self, raw_data):
		processed_rows = []
		for row in raw_data:
			parsed_names = self.name_parser.parse_name(row[self.PROJECT_MEMBERS])
			row[self.PROJECT_MEMBERS] = parsed_names
			processed_rows.append(row)
		return processed_rows


class EngRecDataProjectTransformer(EngRecDataTransformer):

	def transform(self, raw_data):
		processed_rows = []
		for row in raw_data:
			processed_row = self._process_row(row)
			if processed_row:
				processed_rows.append(processed_row)

		return processed_rows

	def _process_row(self, row):
		processed_row = {}
		for external_key, internal_key in self.external_to_internal_field_names_map.iteritems():
			value = row[external_key]
			if value:
				processed_row[internal_key] = value
		return processed_row


class EngRecDataETL(etl.ETL):

	extractor = etl.CSVExtractor()

	transformers = [
		EngRecDataHackathonTransformer(),
		EngRecDataProjectTransformer(),
		EngRecDataProjectMemberTransformer()
	]

	def transform(self):
		current_data = self.raw_data
		for transformer in self.transformers:
			current_data = transformer.transform(current_data)

		self.transformed = current_data

	def load(self):
		pass
