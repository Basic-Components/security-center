import asyncio
import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).absolute().parent.parent.joinpath("security-center")))
from model import db,User
from aioorm.utils import AioDbFactory
import unittest

class ModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        uri = "postgresql://postgres:rstrst@localhost:5432/test"#单位windows
        database = AioDbFactory(uri)
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


    async def _create_table(self):
        await self.db.connect(self.loop)
        await self.db.create_tables([User], safe=True)
        

    async def _drop_table(self):
        await db.drop_tables([User], safe=True)
        await db.close()


    async def _test_user_table_create(self):
        await self._create_table()
        assert await User.table_exists() is True
        await self._drop_table()

    def test_user_table_create(self):
        self.loop.run_until_complete(self._test_user_table_create())


    async def _test_user_create_single(self):
        await self._create_table()
        await User.create_user(nickname=self.nickname, password = self.password, email=self.email)
        #user = await User.get(User.nickname == self.nickname)
        # assert user.nickname == self.nickname
        # assert user.check_password(self.password)
        await self._drop_table()

    def test_user_create_single(self):
        self.loop.run_until_complete(self._test_user_create_single())


def add_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAdd("test_user_table_create"))
    #suite.addTest(TestAdd("test_user_create_single"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = add_suite()
    runner.run(test_suite)
