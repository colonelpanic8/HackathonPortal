import re
import etl


FIRST_NAME_HEADER = 'First'
LAST_NAME_HEADER = 'Last'
EMAIL_HEADER = 'Email'
INF = 99999

class NameParser(object):


	def __init__(self, phonebook='../data/phonebook.csv'):
		self.yelp_engineers = self._get_names_from_phonebook(phonebook)

	def _get_names_from_phonebook(self, phonebook):
		csv_extractor = etl.CSVExtractor()
		phonebook_names = csv_extractor.extract(phonebook)
		return phonebook_names

	def parse_name(self, raw_name):
		comma_separated_names = raw_name.split(",")
		if len(comma_separated_names) > 1:
			matched_names = set([self._match_name(name) for name in comma_separated_names])
		else:
			splitted_names = raw_name.split("\n") if "\n" in raw_name else raw_name.split(" ")
			matched_names = set([self._match_name(name) for name in splitted_names])
		matched_name_list.append(matched_names)
		return matched_name_list

	def _split_by_full_names(self, raw_names):
		full_name_regex = "([A-Z][a-z] [A-Z][a-z] )+"
		re.search(full_name_regex, raw_names)

	def _match_name(self, original_name, threshold=1):
		potential_match = None
		min_distance = INF
		name = original_name.lower()
		for yelp_engineer in self.yelp_engineers:
			first_name = yelp_engineer[FIRST_NAME_HEADER].lower()
			last_name = yelp_engineer[LAST_NAME_HEADER].lower()
			email = yelp_engineer[EMAIL_HEADER].lower()
			handle = email[:email.find('@')]
			full_name = " ".join([first_name, last_name])
			distance = min(
				[
					self.levenshtein(name, first_name),
					self.levenshtein(name, last_name),
					self.levenshtein(name, full_name),
					self.levenshtein(name, email),
					self.levenshtein(name, handle)
				]
			)
			if distance < min_distance:
				min_distance = distance
				potential_match = yelp_engineer[EMAIL_HEADER]
		return potential_match if min_distance <= threshold else original_name

	def levenshtein(self, seq1, seq2):
		oneago = None
		thisrow = range(1, len(seq2) + 1) + [0]
		for x in xrange(len(seq1)):
			twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
			for y in xrange(len(seq2)):
				delcost = oneago[y] + 1
				addcost = thisrow[y - 1] + 1
				subcost = oneago[y - 1] + (seq1[x] != seq2[y])
				thisrow[y] = min(delcost, addcost, subcost)
		return thisrow[len(seq2) - 1]