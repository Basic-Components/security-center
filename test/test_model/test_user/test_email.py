import sys
import asyncio
import unittest
from pathlib import Path
try:
    from security_center.model import User
except:
    path = str(
        Path(__file__).absolute().parent.parent.parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from security_center.model import User
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
    print("setUp model User email test")


def tearDownModule():
    print("tearDown model User email test")


class EmailTest(Core):

    async def _test_user_set_email(self):
        """测试修改邮箱."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        new_email = "zxcv@12345.com"
        user_id = user.uid
        old_cet = user.cemail_time
        old_utime = user.utime
        assert user.changed_history.get("email") is None

        await asyncio.sleep(1)
        await user.set_email(new_email)
        user = await User.get(User.uid == user_id)
        assert user.email == new_email
        assert user.cemail_time != old_cet
        assert user.changed_history.get("email") is not None
        assert user.utime != old_utime
        await self._drop_table()

    def test_user_set_email(self):
        self.loop.run_until_complete(self._test_user_set_email())


def email_suite():
    suite = unittest.TestSuite()
    suite.addTest(EmailTest("test_user_set_email"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = email_suite()
    runner.run(test_suite)
