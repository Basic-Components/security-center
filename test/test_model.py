import asyncio
import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).absolute().parent.parent.joinpath("security-center")))
from model import db, User
from aioorm.utils import AioDbFactory
import unittest
from unittest import mock


class ModelTest(unittest.TestCase):

    # 初始化数据库和连接
    @classmethod
    def setUpClass(cls):
        # uri = "postgresql://postgres:rstrst@localhost:5432/test"#单位windows
        uri = "postgresql://huangsizhe:@localhost:5432/test_ext"
        database = AioDbFactory(uri)
        database.salt = "qwe"
        cls.nickname = 'huangsizhe'
        cls.password = '12345'
        cls.email = "hsz1273327@gmail.com"
        db.initialize(database)
        cls.loop = asyncio.new_event_loop()
        cls.db = db
        asyncio.set_event_loop(cls.loop)

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        cls.loop.close()

    # 创建和删除表

    async def _create_table(self):
        await self.db.connect(self.loop)
        await self.db.create_tables([User], safe=True)

    async def _drop_table(self):
        await db.drop_tables([User], safe=True)
        await db.close()

    # 测试表创建

    async def _test_user_table_create(self):
        await self._create_table()
        assert await User.table_exists() is True
        await self._drop_table()

    def test_user_table_create(self):
        self.loop.run_until_complete(self._test_user_table_create())

    # 测试创建表中一行数据

    async def _test_user_create_single(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.nickname == self.nickname
        assert user.check_password(self.password)
        assert user.email == self.email
        assert len(user.access_authority) == 1
        assert user.access_authority[0]["name"] == 'security-center'
        # for i, v in user.to_dict().items():
        #     print("{}:{}".format(i, v))
        await self._drop_table()

    def test_user_create_single(self):
        self.loop.run_until_complete(self._test_user_create_single())

    async def _test_user_create_app(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email,
            access_authority="newapp"
        )
        user = await User.get(User._nickname == self.nickname)
        assert user.nickname == self.nickname
        assert user.check_password(self.password)
        assert user.email == self.email
        assert len(user.access_authority) == 2
        access_authority_names = [i["name"] for i in user.access_authority]
        assert 'security-center' in access_authority_names
        assert 'newapp' in access_authority_names
        await self._drop_table()

    def test_user_create_app(self):
        self.loop.run_until_complete(self._test_user_create_app())

    # 测试修改密码

    async def _test_user_set_password(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        user = await User.get(User._nickname == self.nickname)
        new_pwd = "zxcv"
        await user.set_password(new_pwd)
        assert not user.check_password(self.password)
        assert user.check_password(new_pwd)
        await self._drop_table()

    def test_user_change_password(self):
        self.loop.run_until_complete(self._test_user_set_password())

    # 测试从session中获取当前的用户

    async def _test_current_user(self):
        await self._create_table()
        await User.create_user(
            nickname=self.nickname,
            password=self.password,
            email=self.email
        )
        _user = await User.get(User._nickname == self.nickname)
        print(type(_user.uid))
        print(_user.uid)
        sessionmock = {"uid":_user.uid}
        user = await User.current_user(sessionmock)
        assert _user == user
        await self._drop_table()

    def test_current_user(self):
        self.loop.run_until_complete(self._test_current_user())



def add_suite():
    suite = unittest.TestSuite()
    suite.addTest(ModelTest("test_user_table_create"))
    suite.addTest(ModelTest("test_user_create_single"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = add_suite()
    runner.run(test_suite)
