from geopy import distance
import numpy as np
import pandas as pd


def score_results(matches, query, loc=None):
    """
    This function scores the town matches according to proportion of letters
    matched in name, distance from coordinates (if provided) and population.

    :param matches: list of OrderedDicts containing matching towns
    :param loc: tuple of latitude and longitude for the query
    :param query: town name to match

    :return: town information ranked by matching confidence with associated
    score in JSON format
    """

    df = pd.DataFrame(matches)
    df['coords'] = list(zip(df['lat'], df['long']))

    if loc:
        # Calculate distance between provided coordinates and those in list
        df['distance'] = df['coords'].apply(distance.distance, args=(loc,))
        df['distance'] = df['distance'].apply(lambda x: x.km)  # get num value
    else:
        df['distance'] = 0

    #  Calculate proportion of letters matched between input and city name
    df['match'] = df['name'].apply(lambda x: len(query) / len(x))

    #  Sort according to match, distance and population
    df = df.sort_values(['match', 'distance', 'population'],
                        ascending=[False, True, False]).reset_index()

    # Score based on number and order of results
    df['score'] = np.round(np.linspace(1, 0, len(df.index)), 2)

    # Remove unnecessary columns and convert back to JSON
    cols = ['fullname', 'lat', 'long', 'score']
    df2 = df[cols]
    df2.columns = ['name', 'latitude', 'longitude', 'score']
    # df2.to_json(orient='records', lines=True)
    df2_list = df2.to_dict('records')

    return df2_list
