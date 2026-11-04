import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

if __name__ == '__main__':
    unittest.main()