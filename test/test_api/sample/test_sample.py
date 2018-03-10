import unittest
try:
    from test.test_api.core import Core
except:
    import sys
    from pathlib import Path
    path = str(
        Path(__file__).absolute().parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from core import Core


def setUpModule():
    print("[SetUp Api Sample test]")


def tearDownModule():
    print("[TearDown Api Sample test]")


class SanicTest(Core):

    def test_get(self):
        request, response = self.app.get('/api/simple')
        self.assertEqual(response.json["message"], 'I am get method')

    def test_post(self):
        request, response = self.app.post('/api/simple')
        self.assertEqual(response.json["message"], 'I am post method')

    def test_put(self):
        request, response = self.app.put('/api/simple')
        self.assertEqual(response.json["message"], 'I am put method')

    def test_delete(self):
        request, response = self.app.delete('/api/simple')
        self.assertEqual(response.json["message"], 'I am delete method')

    def test_patch(self):
        request, response = self.app.patch('/api/simple')
        self.assertEqual(response.json["message"], 'I am patch method')


def ping_suite():
    suite = unittest.TestSuite()
    suite.addTest(SanicTest("test_get"))
    suite.addTest(SanicTest("test_post"))
    suite.addTest(SanicTest("test_put"))
    suite.addTest(SanicTest("test_delete"))
    suite.addTest(SanicTest("test_patch"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = ping_suite()
    runner.run(test_suite)