import unittest
from flask import Flask, session
import json
from server import app, loadClubs, loadCompetitions, loadPlaces

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.data_comps = loadCompetitions()
        self.data_clubs = loadClubs()
        self.data_places = loadPlaces()

    def tearDown(self):
        pass

    def test_home_page(self):
        client = self.app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

        expected_page_name = "Home"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

if __name__ == '__main__':
    unittest.main()
