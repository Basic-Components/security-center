import asyncio
from functools import partial
import aioredis
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
        app.config.update({
            'SESSION_TIMEOUT': 10 * 60,
            'ACTIVATE_TIMEOUT': 5 * 60
        })
        database.salt = app.config.SECRET
        db.initialize(database)
        app.config.update({
            "TEST": True
        })
        cls.client = app.test_client
        cls.db = db
        cls.get_redis_pool = partial(
            aioredis.create_pool,
            app.config.REDIS_URL
        )
        cls.session_pix = app.name + "::Session::"
        print("SetUp Api test context")

    @classmethod
    def tearDownClass(cls):
        print("TearDown Api test context")

    def tearDown(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.clear_db(loop))

    async def clear_db(self, loop):
        try:
            await db.connect(loop)
        except:
            pass
        await db.drop_tables([User], safe=True)
        await db.close()
        print("[drop table done!]")

    async def _create_table(self):
        """创建表."""
        loop = asyncio.new_event_loop()
        await self.db.connect(loop)
        await self.db.create_tables([User], safe=True)

    async def _drop_table(self):
        """删除表."""
        await self.db.drop_tables([User], safe=True)
        await self.db.close()
