import hmac

from aioorm import (
    AioModel,
    AioPostgreSQLDatabase
)

from peewee import (
    Proxy,
    CharField,
    DateTimeField,
)
from playhouse.postgres_ext import (
    JSONField,
    BinaryJSONField
)

db = Proxy()


class BaseModel(AioModel):
    class Meta:
        database = db


class User(BaseModel):
    uid = UUIDField(primary_key=True)
    nickname = CharField(unique=True)
    password = CharField()
    email = CharField()
    ctime = DateTimeField()
    info = BinaryJSONField()

    @staticmethod
    def hash_password(org_pwd):
        salt = self.Meta.database.salt.encode("utf-8")
        org_pwd = org_pwd.encode("utf-8")
        hash_pwd = hmac.new(salt, org_pwd)
        return hash_pwd.hexdigest()

    @classmethod
    async def current_user(clz, session):
        uid = session['uid']
        user = await clz.get(clz.uid == uid)
        return user

    def check_password(self, org_pwd):
        hash_pwd = User.hash_password(org_pwd)
        if self.password == hash_pwd:
            return True
        else:
            return False
