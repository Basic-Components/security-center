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


def user_create_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserCreateTest("test_create"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_create_suite()
    runner.run(test_suite)
