from city_api import (City, get_cities, text_match, score_results,
                      check_inputs)
import unittest
import json


class TestValidators(unittest.TestCase):
    def test_latitude_missing(self):
        """ Test that correct error message is returned when latitude is missing. """
        query = 'test'
        latitude = None
        longitude = '81'
        result = check_inputs(query, latitude, longitude)
        expected = {'error': 'Latitude is missing!'}
        self.assertEqual(result, expected)

    def test_longitude_missing(self):
        """ Test that correct error message is returned when longitude is missing. """
        query = 'test'
        latitude = '36'
        longitude = None
        result = check_inputs(query, latitude, longitude)
        expected = {'error': 'Longitude is missing!'}
        self.assertEqual(result, expected)

    def test_query_with_numbers(self):
        """ Make sure query does not contain numbers. """
        query = 'par1s'
        latitude = '36'
        longitude = '86'
        result = check_inputs(query, latitude, longitude)
        expected = {'error': 'City name must not contain numbers!'}
        self.assertEqual(result, expected)

    def test_not_string_query(self):
        """ Make sure query is string. """
        query = {'city': 'vancouver'}
        latitude = '36'
        longitude = '86'
        result = check_inputs(query, latitude, longitude)
        expected = {'error': 'City name must be a string!'}
        self.assertEqual(result, expected)

    def test_invalid_coord(self):
        query = 'paris'
        latitude = 'thirtysix'
        longitude = '86'
        result = check_inputs(query, latitude, longitude)
        expected = {'error': 'Invalid coordinate(s)'}
        self.assertEqual(result, expected)

    def test_false_when_valid(self):
        """ Returns false when sending a valid query. """
        query = 'paris'
        latitude = '36'
        longitude = '86'
        result = check_inputs(query, latitude, longitude)
        self.assertFalse(result)


class TestTextMatching(unittest.TestCase):
    def test_no_match(self):
        """ Should return empty list if no matches. """
        query = 'doesntexist'
        result = text_match(query)
        self.assertFalse(result)

    def test_valid_match(self):
        """ With valid query, non-empty list should be returned. """
        query = 'paris'
        result = text_match(query)
        self.assertTrue(result)


class TestsScoring(unittest.TestCase):
    def test_same_distance(self):
        """ With same name and no coordinates, results should be sorted by population. """
        query = 'paris'
        cities = get_cities(query)
        pops = [city['population'] for city in cities]
        pops_sorted = sorted(pops, reverse=True)
        self.assertEqual(pops, pops_sorted)

    def test_with_distance(self):
        """ With same name and coordinates provided, results should not be
        sorted by population (except coincidentally...). """
        query = 'paris'
        latitude = '36'
        longitude = '86'
        cities = get_cities(query, latitude, longitude)
        pops = [city['population'] for city in cities]
        pops_sorted = sorted(pops, reverse=True)
        self.assertNotEqual(pops, pops_sorted)


if __name__ == "__main__":
    unittest.main()