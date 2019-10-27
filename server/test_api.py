import unittest
from yuna import app

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_api(self):
        res = self.app.get('/api')
        self.assertEqual(res.status_code, 200)
        self.assertIn('yuna', str(res.data))

def main():
    unittest.main()

if __name__ == "__main__":
    main()
