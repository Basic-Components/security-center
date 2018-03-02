import sys
import unittest
from pathlib import Path
path = str(
    Path(__file__).absolute().parent.parent.parent.parent.joinpath(
        "security-center"
    )
)
if path not in sys.path:
    sys.path.append(path)

from model import User
try:
    from test.test_model.core import Core
except:
    path = str(
        Path(__file__).absolute().parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from core import Core


def setUpModule():
    print("setUp model User GetUser test")


def tearDownModule():
    print("tearDown model User GetUser test")


class GetUserTest(Core):

    async def _test_current_user(self):
        """测试从session中获取当前的用户."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        _user = await User.get(User._nickname == self.nickname)
        sessionmock = {"uid": _user.uid}
        user = await User.current_user(sessionmock)
        assert _user == user
        await self._drop_table()

    def test_current_user(self):
        self.loop.run_until_complete(self._test_current_user())

    async def _test_to_dict(self):
        """测试从to_dict获取当前的用户信息."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        user_dict = user.to_dict()

        for i, v in user_dict.items():
            if i == 'real_name_auth':
                assert v is False
            elif i in ("auth_time", "close_time", "phone"):
                assert v is None
            else:
                assert v is not None
        await self._drop_table()

    def test_to_dict(self):
        self.loop.run_until_complete(self._test_to_dict())


def get_user_suite():
    suite = unittest.TestSuite()
    suite.addTest(GetUserTest("test_current_user"))
    suite.addTest(GetUserTest("test_to_dict"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = get_user_suite()
    runner.run(test_suite)
