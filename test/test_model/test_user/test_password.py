import sys
from datetime import datetime
import unittest
from pathlib import Path
path = str(
    Path(__file__).absolute().parent.parent.parent.parent.joinpath(
        "security-center"
    )
)
if path not in sys.path:
    sys.path.append(path)

from App.model import User
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
    print("setUp model User passwrod test")


def tearDownModule():
    print("tearDown model User passwrod test")


class PasswordTest(Core):

    async def _test_user_set_password(self):
        """测试修改密码."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.changed_history.get("password") is None
        old_utime = user.utime
        new_pwd = "zxcv"
        await user.set_password(new_pwd)
        assert not user.check_password(self.password)
        assert user.check_password(new_pwd)
        assert user.changed_history.get("password") is not None
        assert user.utime != old_utime
        await self._drop_table()

    def test_user_change_password(self):
        self.loop.run_until_complete(self._test_user_set_password())

    # 测试获取密码修改的时间

    async def _test_user_get_cpasswordtime(self):
        """测试获取密码修改的时间."""
        now = datetime.now()
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        user_cpassword_time = datetime.strptime(user.cpassword_time, User.DATETIME_FMT)
        assert user_cpassword_time.year == now.year
        assert user_cpassword_time.month == now.month
        assert user_cpassword_time.day == now.day
        assert user_cpassword_time.hour == now.hour
        assert user_cpassword_time.minute == now.minute
        await self._drop_table()

    def test_user_get_cpasswordtime(self):
        self.loop.run_until_complete(self._test_user_get_cpasswordtime())


def password_suite():
    suite = unittest.TestSuite()
    suite.addTest(PasswordTest("test_user_change_password"))
    suite.addTest(PasswordTest("test_user_get_cpasswordtime"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = password_suite()
    runner.run(test_suite)
