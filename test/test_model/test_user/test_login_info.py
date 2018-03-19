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
    print("setUp model User SocialAccount test")


def tearDownModule():
    print("tearDown model User SocialAccount test")


class LoginInfoTest(Core):

    async def _test_set_login_info(self):
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            self.assertDictEqual(
                user.login_info,
                {
                    'ip': None,
                    'device': None,
                    'city': None,
                    'time': None
                }
            )
            assert user.login_history["last"] is None
            await user.set_login_info(
                ip="119.137.54.34",
                device="pc"
            )
            assert user.login_info.get("ip") == '119.137.54.34'
            assert user.login_info.get("device") == 'pc'
            assert user.login_info.get("city") == '广东省深圳市'
        except:
            raise
        finally:
            await self._drop_table()

    def test_set_login_info(self):
        self.loop.run_until_complete(self._test_set_login_info())

    async def _test_reset_login_info(self):
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            self.assertDictEqual(
                user.login_info,
                {
                    'ip': None,
                    'device': None,
                    'city': None,
                    'time': None
                }
            )
            assert user.login_history["last"] is None
            await user.set_login_info(
                ip="119.137.54.34",
                device="pc"
            )
            await user.set_login_info(
                ip="119.137.54.34",
                device="mobile"
            )
            assert user.login_info.get("ip") == '119.137.54.34'
            assert user.login_info.get("device") == 'mobile'
            assert user.login_info.get("city") == '广东省深圳市'
            assert user.login_history["last"]["device"] == 'pc'
            assert len(user.login_history['statistics']["ip"]) == 1
            assert user.login_history['statistics']["ip"]["119.137.54.34"]["count"] == 1
            await user.set_login_info(
                ip="119.137.54.34",
                device="mobile"
            )
            assert user.login_info.get("ip") == '119.137.54.34'
            assert user.login_info.get("device") == 'mobile'
            assert user.login_info.get("city") == '广东省深圳市'
            assert user.login_history["last"]["device"] == 'mobile'
            assert len(user.login_history['statistics']["ip"]) == 1
            assert user.login_history['statistics']["ip"]["119.137.54.34"]["count"] == 2
        except:
            raise
        finally:
            await self._drop_table()

    def test_reset_login_info(self):
        self.loop.run_until_complete(self._test_reset_login_info())


def social_account_suite():
    suite = unittest.TestSuite()
    suite.addTest(LoginInfoTest("test_set_login_info"))
    suite.addTest(LoginInfoTest("test_reset_login_info"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = social_account_suite()
    runner.run(test_suite)
