from datetime import datetime


class RoleMixin:
    @property
    def role(self):
        return dict(self.ROLE_CHOICES)[self._role]

    async def set_role(self, value: str):
        now = datetime.now()
        real_value = {v: i for i, v in self.ROLE_CHOICES}.get(value)
        if real_value is not None:
            self._role = real_value
            await self.save()
        else:
            raise ValueError("Illegal role")
