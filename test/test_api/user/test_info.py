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


class UserInfoTest(Core):

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

    def test_api_info(self):
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
            '/api/user/', cookies=cookies
        )
        assert "links" in response.json.keys()

    def test_get_user_info(self):
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
            '/api/user/profile', cookies=cookies
        )
        assert response.json["message"]["city"] is None
    @unittest.skip("无法通过api激活用户")
    def test_update_user_info(self):
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
        request, response = self.client.post(
            '/api/user/profile',
            cookies=cookies,
            json={
                "city": "NANTONG"
            }
        )
        assert response.json["message"] == "save done!"
        request, response = self.client.get(
            '/api/user/profile', cookies=cookies
        )
        assert response.json["message"]['city'] == "NANTONG"


def user_info_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserInfoTest("test_api_info"))
    suite.addTest(UserInfoTest("test_get_user_info"))
    suite.addTest(UserInfoTest("test_update_user_info"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_info_suite()
    runner.run(test_suite)
