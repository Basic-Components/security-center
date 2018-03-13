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
    print("[SetUp Api User create test]")


def tearDownModule():
    print("[TearDown Api User create test]")


class UserCreateTest(Core):

    def test_create(self):
        request, response = self.app.post(
            '/api/User',
            json={
                "nickname": 'hsz',
                "password": 'qwer',
                'email': 'hsz1273327@gmail.com'
            }
        )
        #self.assertEqual(response.json["message"], 'I am get method')
        print(response.json["message"])

    # def test_create_from_other_app(self):
    #     request, response = self.app.post(
    #         '/api/User',
    #         json={
    #             "nickname": 'hsz',
    #             "password": 'Qwer123',
    #             'email'
    #         }
    #     )
    #     self.assertEqual(response.json["message"], 'I am get method')


def user_create_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserCreateTest("test_create"))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_create_suite()
    runner.run(test_suite)
