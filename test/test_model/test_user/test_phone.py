import sys
import asyncio
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
    print("setUp model User phone test")


def tearDownModule():
    print("tearDown model User phone test")


class PhoneTest(Core):

    async def _test_user_set_phone(self):
        """测试修改手机号."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        new_phone1 = "123345"
        user_id = user.uid
        old_utime = user.utime
        assert user.cphone_time is None
        assert user.changed_history.get("phone") is None
        await asyncio.sleep(1)
        await user.set_phone(new_phone1)
        user = await User.get(User.uid == user_id)
        old_cet = user.cphone_time
        assert user.phone == new_phone1
        assert user.changed_history.get("phone") is None
        new_phone2 = "32353254"
        await asyncio.sleep(1)
        await user.set_phone(new_phone2)
        assert user.phone == new_phone2
        assert user.cphone_time != old_cet
        assert user.changed_history.get("phone") is not None
        assert user.utime != old_utime
        await self._drop_table()

    def test_user_set_phone(self):
        self.loop.run_until_complete(self._test_user_set_phone())


def phone_suite():
    suite = unittest.TestSuite()
    suite.addTest(PhoneTest("test_user_set_phone"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = phone_suite()
    runner.run(test_suite)
