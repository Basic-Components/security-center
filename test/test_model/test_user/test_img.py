import sys
import unittest
from pathlib import Path
import aiofiles
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
    local = False
except:
    local=True
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


class ImgTest(Core):

    async def _test_user_set_img(self):
        """测试修改用户自定义信息."""
        await self._create_table()
        try:
            await User.create_user(
                nickname=self.nickname,
                password=self.password,
                email=self.email
            )
            user = await User.get(User._nickname == self.nickname)
            user_id = user.uid
            assert user.img_url is None
            if local:
                async with aiofiles.open("./test_img.gif","rb") as f:
                    body = await f.read()
                    new_image = {
                        'type_':'gif',
                        "body":body
                    }
            else:
                async with aiofiles.open("test_img.gif","rb") as f:
                    body = await f.read()
                    new_image = {
                        'type_':'gif',
                        "body":body
                    }

            await user.set_img(**new_image)
            user = await User.get(User.uid == user_id)
            print(len(user.img_url))
            assert user.img_url is not None
        except:
            raise
        finally:
            await self._drop_table()

    def test_user_set_img(self):
        self.loop.run_until_complete(self._test_user_set_img())


def info_suite():
    suite = unittest.TestSuite()
    suite.addTest(ImgTest("test_user_set_img"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = info_suite()
    runner.run(test_suite)
