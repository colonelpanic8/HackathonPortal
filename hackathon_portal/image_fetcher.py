import itertools
import json
import random
import urllib
import urllib2

import config


MAX_IMAGES_TRIED = 5
WGET_TIMEOUT = 1


class TimeOutException(Exception): pass
class NoAvailableImageException(Exception): pass


class ImageFetcher(object):

    DEFAULT_QUERY = "goat"

    def __init__(self, search_term=None):
        self.search_term = search_term or self.DEFAULT_QUERY
        self.random_image_number = random.randint(1, config.MAX_RESULT)

    def _build_search_url(self):
        params = urllib.urlencode(
            dict(
                key=config.API_KEY,
                cx=config.CX,
                searchType="image",
                start=self.random_image_number/config.RES_PER_REQUEST + 1,
                q=self.search_term,
                alt="json",
            )
        )
        return config.API_BASE_URL + '?' + params

    def _fetch_search_results(self):
        return urllib2.urlopen(self._build_search_url()).read()

    def get_my_image(self):
        all_results = json.loads(self._fetch_search_results())
        for _ in itertools.repeat(None, MAX_IMAGES_TRIED):
            my_image = all_results['items'][self.random_image_number % config.RES_PER_REQUEST]
            try:
                urllib2.urlopen(my_image['link'], timeout=WGET_TIMEOUT).read()
            except urllib2.HTTPError:
                continue
            else:
                break
        else:
            raise NoAvailableImageException
        return my_image['link']
