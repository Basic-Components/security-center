import unittest
import asyncio
import ujson

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


class UserloginTest(Core):

    def setUp(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.create_user())

    async def create_user(self):
        await self._create_table()
        await User.create_user(**{
            "nickname": 'hsz',
            "password": 'qwe1Q23',
            'email': 'hsz1273327@gmail.com'
        })

    async def check_session(self, session):
        pool = await self.get_redis_pool()
        async with pool.get() as conn:
            value = await conn.execute('EXISTS', self.session_pix + session)
            assert value
            value = await conn.execute('GET', self.session_pix + session)
            value = ujson.loads(value)["uid"]
        await self.db.connect()
        user = await User.get(User.uid == value)
        assert 'hsz' == user.nickname
        pool.close()
        await pool.wait_closed()
    @unittest.skip("无法通过api激活用户")
    def test_check_right(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz',
                "password": 'qwe1Q23'
            }
        )
        session = response.json["token"]
        cookies = {
            "session": session
        }
        request, response = self.client.get(
            '/api/user/login', params={"application": "security-center"}, cookies=cookies
        )
        assert response.json["can_access"] is True
        request, response = self.client.get(
            '/api/user/login', params={"application": "myapp"}, cookies=cookies
        )
        assert response.json["can_access"] is False

    def test_login_with_nickname(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz',
                "password": 'qwe1Q23'
            }
        )
        session = response.json["token"]
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.check_session(session))

    def test_login_with_email(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz1273327@gmail.com',
                "password": 'qwe1Q23'
            }
        )
        session = response.json["token"]
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.check_session(session))
    @unittest.skip("无法通过api激活用户")
    def test_login_with_application(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz1273327@gmail.com',
                "password": 'qwe1Q23',
                "application": "security-center"
            }
        )
        assert response.json["can_access"] == True

    def test_login_with_no_valid_application(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz1273327@gmail.com',
                "password": 'qwe1Q23',
                "application": "myapp"
            }
        )
        assert response.json["can_access"] == False

    def test_login_unknown_user(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz123',
                "password": 'qwe1Q23'
            }
        )
        assert response.status == 404

    def test_login_pwd_error(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz',
                "password": 'qwe1Q23124'
            }
        )
        assert response.status == 401

    def test_logout_with_session(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz',
                "password": 'qwe1Q23'
            }
        )
        session = response.json["token"]
        cookies = {
            "session": session
        }
        request, response = self.client.delete(
            '/api/user/login', cookies=cookies
        )
        assert response.status == 200

    def test_logout_without_session(self):
        request, response = self.client.delete(
            '/api/user/login'
        )
        assert response.status == 401

    def test_logout_unknown_user(self):
        cookies = {
            "session": "12543d"
        }
        request, response = self.client.delete(
            '/api/user/login', cookies=cookies
        )
        assert response.status == 401


def user_login_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserloginTest("test_check_right"))
    suite.addTest(UserloginTest("test_login_with_nickname"))
    suite.addTest(UserloginTest("test_login_with_email"))
    suite.addTest(UserloginTest("test_login_with_application"))
    suite.addTest(UserloginTest("test_login_with_no_valid_application"))
    suite.addTest(UserloginTest("test_login_unknown_user"))
    suite.addTest(UserloginTest("test_login_pwd_error"))
    suite.addTest(UserloginTest("test_logout_with_session"))
    suite.addTest(UserloginTest("test_logout_without_session"))
    suite.addTest(UserloginTest("test_logout_unknown_user"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_login_suite()
    runner.run(test_suite)
