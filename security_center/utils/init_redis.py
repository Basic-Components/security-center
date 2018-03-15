import aioredis


class Redis:
    """
    A simple wrapper class that allows you to share a connection
    pool across your application.
    """

    def __init__(self, app=None):
        self._pool = None
        self.uri = None
        if app is None:
            pass
        else:
            self.init_app(app)

    def init_app(self, app):
        self.uri = app.config.REDIS_URL
        app.redis_pool = self._pool

        @app.listener('after_server_stop')
        async def close_redis(app, loop):
            # if app.config.TEST:
            #     await db.drop_tables([User], safe=True)
            #     print("[drop table]")
            self._pool.close()
            await self._pool.wait_closed()

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await aioredis.create_pool(
                self.uri,
                minsize=5, maxsize=10)

        return self._pool


redis = Redis()
