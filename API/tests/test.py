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

    def test_test(self):
        self.assertEqual(1, 1)

    def test_voltage_post(self):
        response = self.client.post('/voltage', json={'meas': 9.5, 'device_id': 1})
        self.assertEqual(response.status_code, 201)