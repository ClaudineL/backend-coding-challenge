from text_matching import text_match
from scoring import score_results


def get_cities(q, latitude=None, longitude=None):
    """ Look up names matching query and return JSON list. """
    if latitude and longitude:
        loc = (latitude, longitude)
    else:
        loc = None
    matches = text_match(q)
    scored_matches = score_results(matches, q, loc)
    return scored_matches
