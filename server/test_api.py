import unittest
from yuna import app

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_api(self):
        res = self.app.get('/api')
        self.assertEqual(res.status_code, 200)
        self.assertIn('yuna', str(res.data))
    def test_detect_no_url(self):
        res = self.app.post('/api/detect', data={})
        self.assertEqual(res.status_code, 400)
    def test_detect_bad_url(self):
        res = self.app.post('/api/detect', data={'url': 'https://github.com'})
        self.assertEqual(res.status_code, 400)
    def test_detect_bad_upstream(self):
        res = self.app.post('/api/detect', data={
            'url': 'http://localhost:3000/img/demo.png'
        })
        self.assertEqual(res.status_code, 502)
    def test_detect(self):
        res = self.app.post('/api/detect', data={
            'url': 'https://raw.githubusercontent.com/lightlyss/yuna/master/demo.png'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('bbox', str(res.data))
        self.assertIn('score', str(res.data))

def main():
    unittest.main()

if __name__ == "__main__":
    main()
