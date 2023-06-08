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

    # ######################################################################## #
    # ####################### TEST ABOUT HOME PAGE ########################### #
    # ######################################################################## #

    def test_home_page(self):
        client = self.app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

        expected_page_name = "Home"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    # ######################################################################## #
    # #################### TEST ABOUT DISPLAY CLUB ########################### #
    # ######################################################################## #

    def test_display_point(self):
        client = self.app.test_client()
        response = client.get('/displayPoints')
        self.assertEqual(response.status_code, 200)
        expected_page_name = "Display"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_display_point_without_login(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = None
        response = client.get('/displayPoints')
        self.assertEqual(response.status_code, 200)
        expected_page_name = "Display"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    # ######################################################################## #
    # ######################### TEST ABOUT LOGIN ############################# #
    # ######################################################################## #

    def test_Success_login(self):
        client = self.app.test_client()
        email_test = self.data_clubs[random.randint(0, len(self.data_clubs)-1)]['email']
        form_data = {
            'email': email_test
        }
        with client.session_transaction() as session:
            session['user_p11'] = None

        response = client.post('/showSummary', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "Resume"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_Failed_login(self):
        client = self.app.test_client()
        form_data = {
            'email': 'wrong@mail.com'
        }
        with client.session_transaction() as session:
            session['user_p11'] = None

        response = client.post('/showSummary', data=form_data)
        self.assertEqual(response.status_code, 200)
        
        expected_page_name = "Home"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_logout(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.get('/logout')
        self.assertEqual(response.status_code, 302)

    # ######################################################################## #
    # ###################### TEST REDIRECT IF NOT LOGIN ###################### #
    # ######################################################################## #

    def test_resume_without_login(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = None

        response = client.get('/resume')
        self.assertEqual(response.status_code, 200)

        expected_page_name = "Home"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    def test_book_without_login(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = None

        response = client.get("/book/Tibo%20Inshape%20Tournament/Simply%20Lift")
        self.assertEqual(response.status_code, 200)

        expected_page_name = "Home"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    # ######################################################################## #
    # ######################### TEST PAGE RESUME ############################# #
    # ######################################################################## #

    def test_resume_page(self):
        client = self.app.test_client()
        with client.session_transaction() as session:
            session['user_p11'] = "john@simplylift.co"

        response = client.get("/resume")
        self.assertEqual(response.status_code, 200)

        expected_page_name = "resume"
        rendered_template = response.get_data(as_text=True)
        self.assertIn(expected_page_name, rendered_template)

    # ######################################################################## #
    # ########################## TEST PAGE BOOK ############################## #
    # ######################################################################## #

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

    # ######################################################################## #
    # ########################### TEST PURCHASE ############################## #
    # ######################################################################## #

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
