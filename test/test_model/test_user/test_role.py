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
    print("setUp model User Role test")


def tearDownModule():
    print("tearDown model User Role test")


class RoleTest(Core):

    async def _test_set_admin(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.role == "普通用户"
        await user.set_role("管理员用户")
        assert user.role == "管理员用户"
        assert user._role == 1
        await self._drop_table()

    def test_set_admin(self):
        self.loop.run_until_complete(self._test_set_admin())

    async def _test_set_superuser(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.role == "普通用户"
        await user.set_role("超级用户")
        assert user.role == "超级用户"
        assert user._role == 0
        await self._drop_table()

    def test_set_superuser(self):
        self.loop.run_until_complete(self._test_set_superuser())

    async def _test_set_unknown_role(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.role == "普通用户"
        with self.assertRaisesRegex(ValueError, r"Illegal role"):
            await user.set_role("未知类型用户")
        await self._drop_table()

    def test_set_unknown_role(self):
        self.loop.run_until_complete(self._test_set_unknown_role())


def role_suite():
    suite = unittest.TestSuite()
    suite.addTest(RoleTest("test_set_admin"))
    suite.addTest(RoleTest("test_set_superuser"))
    suite.addTest(RoleTest("test_set_unknown_role"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = role_suite()
    runner.run(test_suite)
