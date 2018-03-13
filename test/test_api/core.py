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
        database.salt = app.config.SECRET
        db.initialize(database)
        app.config.update({
            "TEST":True
        })
        cls.client = app.test_client
        cls.db = db
        print("SetUp Api test context")

    @classmethod
    def tearDownClass(cls):
        print("TearDown Api test context")

    def tearDown(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.clear_db(loop))

    async def clear_db(self,loop):
        await db.connect(loop)
        await db.drop_tables([User], safe=True)
        await db.close()
        print("[drop table done!]")

