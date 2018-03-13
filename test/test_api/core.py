import asyncio
import unittest
from aioorm.utils import AioDbFactory
try:
    from security_center import app
    from security_center.model import db, User
except:
    import sys
    from pathlib import Path
    path = str(
        Path(__file__).absolute().parent.parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from security_center import app
    from security_center.model import db, User


class Core(unittest.TestCase):
    # 初始化数据库和连接
    @classmethod
    def setUpClass(cls):
        database = AioDbFactory(app.config.TEST_DB_URL)
        db.initialize(database)
        cls.app = app.test_client
        cls.loop = asyncio.new_event_loop()
        cls.db = db
        asyncio.set_event_loop(cls.loop)
        print("SetUp Api test context")

    @classmethod
    def tearDownClass(cls):
        print("TearDown Api test context")

    def setUp(self):
        self.loop.run_until_complete(self._create_table())
        print("instance setUp")

    def tearDown(self):
        print("instance tearDown")

    async def _create_table(self):
        """创建表."""
        await self.db.connect(self.loop)
        await self.db.create_tables([User], safe=True)

    async def _drop_table(self):
        """删除表."""
        await self.db.drop_tables([User], safe=True)
        await self.db.close()
