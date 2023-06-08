import unittest
from flask import Flask, session
import json
from server import app, loadClubs, loadCompetitions, loadPlaces
import random

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.data_comps = loadCompetitions()
        self.data_clubs = loadClubs()
        self.data_places = loadPlaces()

    def tearDown(self):
        pass

    def test_book_page(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.get("/book/Tibo%20Inshape%20Tournament/Simply%20Lift")
        self.assertEqual(response.status_code, 200)

        expected_page_name = "Book"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_book_page_wrong_url(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.get("/book/Tape%20Tournament/Simply%20Lift")
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
