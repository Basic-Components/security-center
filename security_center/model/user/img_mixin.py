import base64
from datetime import datetime
from peewee import (
    CharField,
    TextField
)
from ..base import BaseModel


class ImgMixin(BaseModel):

    # 用户头像
    _img_type = CharField(null=True)
    _img_base64 = TextField(null=True)

    @property
    def img_url(self):
        if self._img_type is None or self._img_base64 is None:
            return None
        else:
            temp = f"data:image/{self._img_type};base64,{self._img_base64}"
        return temp

    async def set_img(self, type_, body):
        self._img_type = type_
        self._img_base64 = base64.b64encode(body).decode("ascii")
        now = datetime.now()
        self._update_time = now
        await self.save()
