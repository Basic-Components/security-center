from datetime import datetime
from peewee import IntegerField
from ..base import BaseModel


class StatusMixin(BaseModel):
    STATUS_CHOICES = ((0, "未认证"), (1, "已认证"), (2, "已注销"))
    # 账户状态,
    _status = IntegerField(default=0, choices=STATUS_CHOICES)

    @property
    def status(self):
        return dict(self.STATUS_CHOICES)[self._status]

    async def set_status(self, value: str):
        now = datetime.now()
        real_value = {v: i for i, v in self.STATUS_CHOICES}.get(value)
        if real_value is not None:
            self._status = real_value
            self._update_time = now
            now = datetime.now()
            if real_value == 1:
                self._auth_time = now
            elif real_value == 2:
                self._close_time = now
            await self.save()
        else:
            raise ValueError("Illegal status")
