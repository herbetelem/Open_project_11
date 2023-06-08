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

    def test_Success_purchase(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'Tibo Inshape Tournament',
            'club': 'Simply Lift',
            'places': '3'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "Resume"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_fail_purchase_unknown_club(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'Tibo Inshape Tournament',
            'club': 'Simply Lt',
            'places': '3'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_fail_purchase_unknown_tournament(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'Tibo Tournament',
            'club': 'Simply Lift',
            'places': '3'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_fail_purchase_too_much_place(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'Tibo Inshape Tournament',
            'club': 'Simply Lift',
            'places': '13'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "book"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_fail_purchase_no_place_up(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'MDI',
            'club': 'Simply Lift',
            'places': '3'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "book"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_fail_purchase_no_pts(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'Tibo Inshape Tournament',
            'club': 'Iron Temple',
            'places': '3'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "admin@irontemple.com"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "book"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_fail_purchase_passed_comp(self):
        client = self.app.test_client()
        
        form_data = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '3'
        }
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.post('/purchasePlaces', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "book"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

if __name__ == '__main__':
    unittest.main()
