import unittest
import os.path
from core import Code, afd

class CoreTest(unittest.TestCase):
    def test_bad_url(self):
        res = afd('https://github.com')
        self.assertEqual(res, Code.EUPSTREAM)

    def test_bad_upstream(self):
        res = afd('http://localhost:3000/img/banner.jpg')
        self.assertEqual(res, Code.EUPSTREAM)

    def test_security(self):
        res = afd('file:///yuna/static/index.png')
        self.assertEqual(res, Code.EUPSTREAM)

    def test_detection(self):
        res = afd('https://raw.githubusercontent.com/lightlyss/yuna/master/banner.png')
        self.assertEqual(len(res), 1)
        self.assertIn('.png', res[0])
        self.assertIn('cache/', res[0])
        self.assertEqual(os.path.isfile(res[0]), True)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
