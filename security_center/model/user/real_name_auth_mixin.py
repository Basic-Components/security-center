from datetime import datetime


class RealNameAuthMixin:
    @property
    def real_name_auth(self):
        return self._real_name_auth

    async def set_real_name_authed(self):
        if self._real_name_auth is True:
            raise ValueError("already real name auth")
        else:
            now = datetime.now()
            self._real_name_auth = True
            self._real_name_auth_time = now
            self._update_time = now
            await self.save()

    @property
    def real_name_auth_time(self):
        return self._time_to_str("real_name_auth")
