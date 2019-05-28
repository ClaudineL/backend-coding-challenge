from geopy import distance
from numpy import linspace, around
from operator import attrgetter
from text_matching import subset_keys


class City:
    """ Create a city object from an OrderedDict. """
    def __init__(self, od, query, loc=None, score=None):
        self.name = od['fullname']
        self.latitude = od['lat']
        self.longitude = od['long']
        self.population = int(od['population'])
        self.match = len(query) / len(self.name.split(',')[0])
        self.score = score

        if loc:
            self.distance = distance.distance((self.latitude, self.longitude),loc).km
        else:
            self.distance = 0

    def __repr__(self):
        return repr((self.name, self.population))


def score_results(matches, query, loc=None):
    """
    This function scores the town matches according to proportion of letters
    matched in name, distance from coordinates (if provided) and population.

    :param matches: list of OrderedDicts containing matching towns
    :param query: town name to match
    :param loc: tuple of latitude and longitude for the query

    :return: list of cities ranked by matching confidence with associated
    score
    """
    city_objects = [City(od, query, loc) for od in matches]

    s = sorted(city_objects, key=attrgetter('population'), reverse=True)
    s = sorted(s, key=attrgetter('distance'), reverse=False)
    s = sorted(s, key=attrgetter('match'), reverse=True)

    # Adding scores
    scores = around(linspace(1, 0, len(s)), 2)
    for city, score in zip(s, scores):
        city.score = score

    # Remove unnecessary fields and return as list of OrderedDicts
    city_dictlist = []
    for city in s:
        city_dict = subset_keys(vars(city), 'name', 'latitude', 'longitude',
                                'population', 'score')
        city_dictlist.append(city_dict)

    return city_dictlist
