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


class SocialAccountTest(Core):

    async def _test_set_social_account(self):
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            assert user.social_accounts is None
            await user._set_social_accounts({
                "google": 'hsz1273327@gmail.com'
            })
            assert [i for i, v in user.social_accounts.items() if i == "google" and v == "hsz1273327@gmail.com"] != []
        except:
            raise
        finally:
            await self._drop_table()

    def test_set_social_account(self):
        self.loop.run_until_complete(self._test_set_social_account())

    async def _test_update_social_account(self):
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            assert user.social_accounts is None
            await user.update_social_accounts(google='hsz1273327@gmail.com')
            assert [i for i, v in user.social_accounts.items() if i == "google" and v == "hsz1273327@gmail.com"] != []
            await user.update_social_accounts(google='hsz1277@gmail.com')
            assert [i for i, v in user.social_accounts.items() if i == "google" and v == "hsz1277@gmail.com"] != []
        except:
            raise
        finally:
            await self._drop_table()

    def test_update_social_account(self):
        self.loop.run_until_complete(self._test_update_social_account())

    async def _test_remove_social_account(self):
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            assert await user.remove_social_accounts("google") is False
            assert user.social_accounts is None
            await user.update_social_accounts(google='hsz1273327@gmail.com')
            assert [i for i, v in user.social_accounts.items() if i == "google" and v == "hsz1273327@gmail.com"] != []
            await user.remove_social_accounts("google")
            assert user.social_accounts["google"] == None

        except:
            raise
        finally:
            await self._drop_table()

    def test_remove_social_account(self):
        self.loop.run_until_complete(self._test_remove_social_account())


def social_account_suite():
    suite = unittest.TestSuite()
    suite.addTest(SocialAccountTest("test_set_social_account"))
    suite.addTest(SocialAccountTest("test_update_social_account"))
    suite.addTest(SocialAccountTest("test_remove_social_account"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = social_account_suite()
    runner.run(test_suite)
