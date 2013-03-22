import re


INF = 99999


def only_one(a_list):
    item, = a_list
    return item


def remap_keys(original_dictionary, key_remapping, value_function=None):
    if value_function is None:
        value_function = lambda x: x
    remapped_dictionary = {}
    for key, value in original_dictionary.iteritems():
        remapped_dictionary[key_remapping.get(key, key)] = value_function(value)
    return remapped_dictionary


def levenshtein(seq1, seq2):
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


class NameParser(object):

    def __init__(self, yelp_engineers):
        self.yelp_engineers = yelp_engineers

    def parse_name(self, raw_name):
        comma_separated_names = raw_name.split(",")
        if len(comma_separated_names) > 1:
            matched_names = set([self._match_name(name) for name in comma_separated_names])
        else:
            splitted_names = raw_name.split("\n") if "\n" in raw_name else raw_name.split(" ")
            matched_names = set([self._match_name(name) for name in splitted_names])
        return matched_names

    def _split_by_full_names(self, raw_names):
        full_name_regex = "([A-Z][a-z] [A-Z][a-z] )+"
        re.search(full_name_regex, raw_names)

    def _match_name(self, original_name, threshold=1):
        potential_match = None
        min_distance = INF
        name = original_name.lower()

        for yelp_engineer in self.yelp_engineers:
            full_name = yelp_engineer.name.lower() if yelp_engineer.name else ''
            email = yelp_engineer.yelp_handle.lower()
            handle = email[:email.find('@')]
            first_name = ''
            last_name = ''
            if full_name:
                first_name, last_name = full_name.rsplit(" ", 1)

            distance = min(
                [
                    levenshtein(name, first_name),
                    levenshtein(name, last_name),
                    levenshtein(name, full_name),
                    levenshtein(name, email),
                    levenshtein(name, handle)
                ]
            )
            if distance < min_distance:
                min_distance = distance
                potential_match = yelp_engineer.yelp_handle
        return potential_match if min_distance <= threshold else original_name