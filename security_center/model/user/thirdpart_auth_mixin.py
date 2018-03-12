from datetime import datetime


class ThirdPartAuthMixin:
    @property
    def thirdpart_auth(self):
        return self._thirdpart_auth

    async def set_thirdpart_auth(self, new_value):
        self._thirdpart_auth = new_value
        self._update_time = datetime.now()
        await self.save()
