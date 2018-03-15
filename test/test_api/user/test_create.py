import unittest
import asyncio
try:
    from test.test_api.core import Core, User
except:
    import sys
    from pathlib import Path
    path = str(
        Path(__file__).absolute().parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from core import Core, User


def setUpModule():
    print("[SetUp Api User create test]")


def tearDownModule():
    print("[TearDown Api User create test]")


class UserCreateTest(Core):

    async def check_user_nickname(self, nickname, uid, loop):
        await self.db.connect(loop)
        user = await User.get(uid=uid)
        assert nickname == user.nickname

    def test_create(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwer123Q',
                'email': 'hsz1273327@gmail.com'
            }
        )
        uid = response.json["message"]
        assert response.status == 200
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.check_user_nickname('hsz', uid, loop))

    def test_app_create(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwer123Q',
                'email': 'hsz1273327@gmail.com',
                "access_authority":"myapp"
            }
        )
        uid = response.json["message"]
        assert response.status == 200
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.check_user_nickname('hsz', uid, loop))

    def test_create_param_lack(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwer123Q'
            }
        )
        uid = response.json["message"]
        assert response.status == 501

    def test_create_with_role(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwer123Q',
                'email': 'hsz1273327@gmail.com',
                'role': "管理员"
            }
        )
        uid = response.json["message"]
        assert response.status == 502

    def test_create_email_error(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwer123Q',
                'email': 'hsz1273327com'
            }
        )
        uid = response.json["message"]
        assert response.status == 503

    def test_create_pw_len_error(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwe1Q',
                'email': 'hsz1273327@gmail.com'
            }
        )
        uid = response.json["message"]
        assert response.status == 504

    def test_create_pw_form_error(self):
        request, response = self.client.post(
            '/api/user',
            json={
                "nickname": 'hsz',
                "password": 'qwe132',
                'email': 'hsz1273327@gmail.com'
            }
        )
        uid = response.json["message"]
        assert response.status == 505


def user_create_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserCreateTest("test_create"))
    suite.addTest(UserCreateTest("test_app_create"))
    suite.addTest(UserCreateTest("test_create_param_lack"))
    suite.addTest(UserCreateTest("test_create_with_role"))
    suite.addTest(UserCreateTest("test_create_email_error"))
    suite.addTest(UserCreateTest("test_create_pw_len_error"))
    suite.addTest(UserCreateTest("test_create_pw_form_error"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_create_suite()
    runner.run(test_suite)
