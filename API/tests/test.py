import unittest
from app import create_app, db

class APITestCase(unittest.TestCase):


    # Set up the environment that the tests will run in
    def setUp(self):
        self.API_KEY = "secretkey1" 
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    # Test that a voltage meas can be posted correctly
    def test_voltage_post_success(self):
        response = self.client.post(f'/voltage?apikey={self.API_KEY}', json={'meas': 9.5, 'device_id': 1})
        self.assertEqual(response.status_code, 201)
    
    # Test that a voltage meas post with invalid data will respond with appropriate codes
    def test_voltage_post_fail(self):
        response = self.client.post('/voltage', json={'meas': "fail", 'device_id': 1})
        self.assertEqual(response.status_code, 400)

    # Test that a current meas can be posted correctly
    def test_current_post_success(self):
        response = self.client.post('/current', json={'meas': 0.1, 'device_id': 1})
        self.assertEqual(response.status_code, 201)

    # Test that a current meas post with invalid data will respond with appropriate codes
    def test_current_post(self):
        response = self.client.post('/current', json={'meas': "fail", 'device_id': 1})
        self.assertEqual(response.status_code, 400)
    
    # Check that voltage closest responds with correct codes for success and error
    def test_voltage_get_closest(self):
        response = self.client.get('/voltage/closest?timestamp=2023-11-21T16:01:00')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/voltage/closest?timestamp=2023-11-2')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/voltage/closest')
        self.assertEqual(response.status_code, 400)
    
    # Check that current closest responds with correct codes for success and error
    def test_current_get_closest(self):
        response = self.client.get('/current/closest?timestamp=2023-11-21T16:01:00')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/current/closest?timestamp=2023-11-2')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/current/closest')
        self.assertEqual(response.status_code, 400)