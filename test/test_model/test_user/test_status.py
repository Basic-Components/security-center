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
    print("setUp model User Status test")


def tearDownModule():
    print("tearDown model User Status test")


class StatusTest(Core):

    async def _test_set_status_authed(self):
        """测试设置用户帐号状态为以认证."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.status == "未认证"
        assert user.auth_time is None
        assert user.close_time is None
        await user.set_status("已认证")
        assert user.status == "已认证"
        assert user._status == 1
        assert user.auth_time is not None
        assert user.close_time is None
        with self.assertRaisesRegex(ValueError, r"Illegal status"):
            await user.set_status("未注销")
        await self._drop_table()

    def test_set_status_authed(self):
        self.loop.run_until_complete(self._test_set_status_authed())

    async def _test_set_status_close(self):
        """测试设置用户帐号状态为已注销."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.status == "未认证"
        assert user.auth_time is None
        assert user.close_time is None
        await user.set_status("已注销")
        assert user.status == "已注销"
        assert user._status == 2
        assert user.auth_time is None
        assert user.close_time is not None
        await self._drop_table()

    def test_set_status_close(self):
        self.loop.run_until_complete(self._test_set_status_close())

    async def _test_set_unknown_status(self):
        """测试设置错误的用户帐号状态."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.status == "未认证"
        assert user.auth_time is None
        assert user.close_time is None
        with self.assertRaisesRegex(ValueError, r"Illegal status"):
            await user.set_status("未注销")
        await self._drop_table()

    def test_set_unknown_status(self):
        self.loop.run_until_complete(self._test_set_unknown_status())


def status_suite():
    suite = unittest.TestSuite()
    suite.addTest(StatusTest("test_set_status_authed"))
    suite.addTest(StatusTest("test_set_status_close"))
    suite.addTest(StatusTest("test_set_unknown_status"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = status_suite()
    runner.run(test_suite)
