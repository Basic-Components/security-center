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
            value = await conn.execute('get', '')
            print('raw value:', value)

    def test_login(self):
        request, response = self.client.post(
            '/api/user/login',
            json={
                "username": 'hsz',
                "password": 'qwe1Q23'
            }
        )
        print(response.json)
        #loop = asyncio.new_event_loop()
        # loop.run_until_complete(self.check_session(session))


def user_create_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserloginTest("test_login"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_create_suite()
    runner.run(test_suite)
