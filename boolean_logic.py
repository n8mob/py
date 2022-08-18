import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertNotEqual(True, False, 'True and False should not be equal')  # add assertion here
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertTrue(True and True)
        self.assertTrue(True or False)
        self.assertFalse(False or False)
        self.assertTrue((True and True) and (False or True))


if __name__ == '__main__':
    unittest.main()
