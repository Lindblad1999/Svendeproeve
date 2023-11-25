import unittest
from app import create_app, db

class APITestCase(unittest.TestCase):

    # Set up the environment that the tests will run in
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def test_voltage_post(self):
        response = self.client.post('/voltage', json={'meas': 9.5, 'device_id': 1})
        self.assertEqual(response.status_code, 201)
    
    def test_current_post(self):
        response = self.client.post('/current', json={'meas': 1.5, 'device_id': 1})
        self.assertEqual(response.status_code, 201)
    
    def test_voltage_get_closest(self):
        response = self.client.get('/voltage/closest?timestamp=2023-11-21T16:01:00')
        self.assertEqual(response.status_code, 200)