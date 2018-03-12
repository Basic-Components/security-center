import sys
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
    print("setUp model User Real Name Auth test")


def tearDownModule():
    print("tearDown model User Real Name Auth test")


class RealNameAuthTest(Core):

    async def _test_real_name_auth(self):
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            assert user.real_name_auth is False
            assert user.real_name_auth_time is None
            await user.set_real_name_authed()
            assert user.real_name_auth is True
            assert user.real_name_auth_time is not None
            with self.assertRaisesRegex(ValueError, r"already real name auth"):
                await user.set_real_name_authed()
        except:
            raise
        finally:
            await self._drop_table()

    def test_real_name_auth(self):
        self.loop.run_until_complete(self._test_real_name_auth())


def role_suite():
    suite = unittest.TestSuite()
    suite.addTest(RealNameAuthTest("test_real_name_auth"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = role_suite()
    runner.run(test_suite)
