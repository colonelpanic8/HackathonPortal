import etl
import logic
import util


HACKATHON_ID = 'HackathonID'
PROJECT_MEMBERS = "ProjectMembers"
PROJECT_DESC = "ProjectDescription"
PROJECT_NAME = "ProjectName"
HACKATHON_STR = 'H@ckathon '


class EngRecDataTransformer(etl.Transformer):

	external_to_internal_field_names_map = {
		"Project Name": PROJECT_NAME,
		"ALL People on Your Team": PROJECT_MEMBERS,
		"What's your project about? Give us some deets! ": PROJECT_DESC,
		"HackathonID": HACKATHON_ID
	}

class EngRecDataHackathonTransformer(EngRecDataTransformer):

	def transform(self, raw_data):
		current_hackathon_id = None
		data_with_hackathon_details = []
		for row in raw_data:
			if HACKATHON_STR in row['Timestamp']:
				raw_hackathon_id = row['Timestamp']
				current_hackathon_id = raw_hackathon_id[
					raw_hackathon_id.find(HACKATHON_STR)+len(HACKATHON_STR):raw_hackathon_id.find('.0')
				]
			else:
				row[HACKATHON_ID] = current_hackathon_id
				data_with_hackathon_details.append(row)

		return data_with_hackathon_details


class EngRecDataProjectMemberTransformer(EngRecDataTransformer):

	def __init__(self):
		self.name_parser = util.NameParser(
			logic.get_all_persons()
		)

	def transform(self, raw_data):
		processed_rows = []
		for row in raw_data:
			parsed_names = self.name_parser.parse_name(row[PROJECT_MEMBERS])
			row[PROJECT_MEMBERS] = parsed_names
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
			processed_row[internal_key] = row[external_key]
		return processed_row


class EngRecDataLoader(etl.Loader):

	def load(self, projects):
		for project in projects:
			logic.add_project(
				project[PROJECT_NAME],
				project[PROJECT_DESC],
				project[PROJECT_MEMBERS],
				project[HACKATHON_ID]
			)


class EngRecDataETL(etl.ETL):

	extractor = etl.CSVExtractor()

	transformers = [
		EngRecDataHackathonTransformer(),
		EngRecDataProjectTransformer(),
		EngRecDataProjectMemberTransformer()
	]

	loader = EngRecDataLoader()

	def transform(self):
		current_data = self.raw_data
		for transformer in self.transformers:
			current_data = transformer.transform(current_data)

		self.transformed = current_data

