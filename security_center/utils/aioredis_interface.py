try:
    import ujson
except:
    import json as ujson
from sanic_session.base import BaseSessionInterface, SessionDict
import uuid

from typing import Callable


class RedisSessionInterface(BaseSessionInterface):
    def __init__(
            self, redis_getter: Callable,
            domain: str=None, expiry: int = 2592000,
            httponly: bool=True, cookie_name: str='session',
            prefix: str='session:'):
        """Initializes a session interface backed by Redis.
        Args:
            redis_getter (Callable):
                Coroutine which should return an asyncio_redis connection pool
                (suggested) or an asyncio_redis Redis connection.
            domain (str, optional):
                Optional domain which will be attached to the cookie.
            expiry (int, optional):
                Seconds until the session should expire.
            httponly (bool, optional):
                Adds the `httponly` flag to the session cookie.
            cookie_name (str, optional):
                Name used for the client cookie.
            prefix (str, optional):
                Memcache keys will take the format of `prefix+session_id`;
                specify the prefix here.
        """
        self.redis_getter = redis_getter
        self.expiry = expiry
        self.prefix = prefix
        self.cookie_name = cookie_name
        self.domain = domain
        self.httponly = httponly

    async def open(self, request):
        """Opens a session onto the request. Restores the client's session
        from Redis if one exists.The session data will be available on
        `request.session`.
        Args:
            request (sanic.request.Request):
                The request, which a sessionwill be opened onto.
        Returns:
            dict:
                the client's session data,
                attached as well to `request.session`.
        """
        sid = request.cookies.get(self.cookie_name)

        if not sid:
            sid = uuid.uuid4().hex
            session_dict = SessionDict(sid=sid)
        else:
            redis_pool = await self.redis_getter()
            async with redis_pool.get() as conn:
                val = await conn.execute('get', self.prefix + sid)
                if val is not None:
                    data = ujson.loads(val)
                    session_dict = SessionDict(data, sid=sid)
                else:
                    session_dict = SessionDict(sid=sid)

        request['session'] = session_dict
        return session_dict

    async def save(self, request, response) -> None:
        """Saves the session into Redis and returns appropriate cookies.
        Args:
            request (sanic.request.Request):
                The sanic request which has an attached session.
            response (sanic.response.Response):
                The Sanic response. Cookies with the appropriate expiration
                will be added onto this response.
        Returns:
            None
        """
        if 'session' not in request:
            return

        redis_pool = await self.redis_getter()
        key = self.prefix + request['session'].sid
        if not request['session']:
            async with redis_pool.get() as conn:
                await conn.execute('DEL', key)

            if request['session'].modified:
                self._delete_cookie(request, response)

            return

        val = ujson.dumps(dict(request['session']))
        async with redis_pool.get() as conn:
            await conn.execute("SETEX", key, self.expiry, val)

        self._set_cookie_expiration(request, response)
