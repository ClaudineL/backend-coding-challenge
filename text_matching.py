from collections import OrderedDict
from pathlib import Path
import csv
import re

CITY_PATH = Path('./data/cities_canada-usa_reformat.tsv')

def text_match(text):
    """ Find cities that match input text. """
    city_array = []
    with CITY_PATH.open(encoding='utf-8', newline='') as city_file:
        city_reader = csv.DictReader(city_file, delimiter='\t',
                                     quoting=csv.QUOTE_NONE)

        for row in city_reader:
            if re.search(text, row['name'], re.IGNORECASE):

                row['fullname'] = ", ".join([row['name'], row['admin1'],
                                             row['country']])

                row2 = subset_keys(row, 'fullname', 'name', 'lat', 'long',
                                   'country', 'admin1', 'population')

                city_array.append(row2)

    return city_array


def subset_keys(d, *keys):
    """ Subset given keys in a dictionary in the order provided. """
    return OrderedDict([(key, d[key]) for key in keys])
