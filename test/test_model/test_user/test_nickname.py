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
    print("setUp model User Nickname test")


def tearDownModule():
    print("tearDown model User Nickname test")


class NicknameTest(Core):

    async def _test_user_set_password(self):
        """测试修改昵称."""
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            new_nickname = "zxcv"
            user_id = user.uid
            old_cnt = user.cnickname_time
            old_utime = user.utime
            assert user.changed_history.get("nickname") is None
            await asyncio.sleep(1)
            await user.set_nickname(new_nickname)
            user = await User.get(User.uid == user_id)
            assert user.nickname == new_nickname
            assert user.cnickname_time != old_cnt
            assert user.changed_history.get("nickname") is not None
            assert user.utime != old_utime
        except:
            raise
        finally:
            await self._drop_table()

    def test_user_set_password(self):
        self.loop.run_until_complete(self._test_user_set_password())

    async def _test_user_reset_password(self):
        """测试修改昵称."""
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            new_nickname = "zxcv"
            user_id = user.uid
            old_cnt = user.cnickname_time
            old_utime = user.utime
            assert user.changed_history.get("nickname") is None
            await user.set_nickname(new_nickname)
            user = await User.get(User.uid == user_id)
            assert user.nickname == new_nickname
            assert user.changed_history.get("nickname") is not None
            new_new_nickname = "des"
            user = await User.get(User.uid == user_id)
            await user.set_nickname(new_new_nickname)
            nicknames = user.changed_history.get("nickname")
            old_names = [i["value"] for i in nicknames]
            assert new_nickname in old_names
        except:
            raise
        finally:
            await self._drop_table()

    def test_user_reset_password(self):
        self.loop.run_until_complete(self._test_user_reset_password())


def nickname_suite():
    suite = unittest.TestSuite()
    suite.addTest(NicknameTest("test_user_set_password"))
    suite.addTest(NicknameTest("test_user_reset_password"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = nickname_suite()
    runner.run(test_suite)
