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
    print("setUp model User info test")


def tearDownModule():
    print("tearDown model User info test")


class InfoTest(Core):

    async def _test_user_set_info(self):
        """测试修改用户自定义信息."""
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        user_id = user.uid
        new_info = {
            'URL': "www.google.cn",
            "bio": "事实事实上",
            "company": "一个企业",
            'nation': "中国",
            'city': "深圳",
        }
        await user.set_info(**new_info)
        user = await User.get(User.uid == user_id)
        self.assertDictEqual(user.info, new_info)
        await self._drop_table()

    def test_user_set_info(self):
        self.loop.run_until_complete(self._test_user_set_info())


def info_suite():
    suite = unittest.TestSuite()
    suite.addTest(InfoTest("test_user_set_info"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = info_suite()
    runner.run(test_suite)
