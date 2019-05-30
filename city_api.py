from geopy import distance
from numpy import linspace, around
from operator import attrgetter
from pathlib import Path
import csv
import markdown
import re

CITY_PATH = Path('./data/cities_canada-usa_reformat.tsv')
MARKDOWN_PATH = Path('./data/api.md')

class City:
    """ Create a city object from a dictionary. """
    def __init__(self, d, query, loc=None, score=None):
        self.name = d['fullname']
        self.latitude = d['lat']
        self.longitude = d['long']
        self.population = int(d['population'])
        self.match = len(query) / len(self.name.split(',')[0])
        self.score = score

        if loc:
            self.distance = distance.distance((self.latitude, self.longitude),loc).km
        else:
            self.distance = 0

    def __repr__(self):
        return repr((self.name, self.population))


def load_md():
    """ Return markdown object from markdown file. """
    with MARKDOWN_PATH.open(encoding='utf-8') as md_file:
        md = markdown.markdown(md_file.read())
    return md

def get_cities(q, latitude=None, longitude=None):
    """ Look up names matching query and return JSON list. """
    if latitude and longitude:
        loc = (latitude, longitude)
    else:
        loc = None
    matches = text_match(q)
    scored_matches = score_results(matches, q, loc)
    return scored_matches


def text_match(text):
    """ Find cities that match input text.

    :param text: town name to match

    :return: list of cities with query text in the name
    """
    city_array = []
    with CITY_PATH.open(encoding='utf-8', newline='') as city_file:
        city_reader = csv.DictReader(city_file, delimiter='\t',
                                     quoting=csv.QUOTE_NONE)

        for row in city_reader:
            if re.search(text, row['name'], re.IGNORECASE):

                row['fullname'] = ", ".join([row['name'], row['admin1'],
                                             row['country']])

                row_clean = subset_keys(row, 'fullname', 'name', 'lat', 'long',
                                   'country', 'admin1', 'population')

                city_array.append(row_clean)

    return city_array


def subset_keys(d, *keys):
    """ Subset given keys in a dictionary in the order provided. """
    return dict([(key, d[key]) for key in keys])


def score_results(matches, query, loc=None):
    """
    This function scores the town matches according to proportion of letters
    matched in name, distance from coordinates (if provided) and population.

    :param matches: list of dictionaries containing matching towns
    :param query: town name to match
    :param loc: tuple of latitude and longitude for the query, optional

    :return: list of cities ranked by matching confidence with associated
    score
    """
    city_objects = [City(d, query, loc) for d in matches]

    s = sorted(city_objects, key=attrgetter('population'), reverse=True)
    s = sorted(s, key=attrgetter('distance'), reverse=False)
    s = sorted(s, key=attrgetter('match'), reverse=True)

    # Adding scores
    scores = around(linspace(1, 0, len(s)), 2)
    for city, score in zip(s, scores):
        city.score = score

    # Remove unnecessary fields and return as list of dicts
    city_dictlist = []
    for city in s:
        city_dict = subset_keys(vars(city), 'name', 'latitude', 'longitude',
                                'population', 'score')
        city_dictlist.append(city_dict)

    return city_dictlist

def check_inputs(query, latitude, longitude):
    """ Perform various checks on inputs.

    All the inner functions return False if the parameter(s) pass(es) the
    checks, or an error message formatted as a dictionary to be parsed by jsonify() in the main code.

    :param query: town name to match
    :param latitude: latitude input or None
    :param longitude: longitude input or None

    :return: False or a dictionary with the relevant error message
    """

    def invalid_query(query):
        """ Make sure query is a string. """
        if isinstance(query, str):
            if re.search(r"[0-9]", query, re.UNICODE):
                return {'error': 'City name must not contain numbers!'}
            else:
                return False
        else:
            return {'error': 'City name must be a string!'}

    def missing_coords(latitude, longitude):
        """ Make sure either both or no coordinates are present. """
        if (latitude and longitude):
            return False
        elif (not latitude and longitude):
            return {'error': 'Latitude is missing!'}
        elif (latitude and not longitude):
            return {'error': 'Longitude is missing!'}
        else:
            return False

    def invalid_coords(coords):
        """ Make sure coordinates are valid numbers """
        for coord in coords:
            if coord:
                try:
                    float(coord)
                    return False
                except ValueError:
                    return {'error': 'Invalid coordinate(s)'}

    # Is query an invalid string?
    check = invalid_query(query)
    if not check:
        # Is one of the coordinates missing?
        check = missing_coords(latitude, longitude)
        if not check:
            # Are the coordinates unable to be parsed as floats?
            check = invalid_coords([latitude, longitude])

    return check