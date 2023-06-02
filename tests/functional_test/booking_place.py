import unittest
from flask import Flask, session
from server import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True

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

if __name__ == '__main__':
    unittest.main()
