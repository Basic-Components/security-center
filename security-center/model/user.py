"""定义user."""
import hmac
from peewee import (
    CharField,
    DateTimeField,
    UUIDField
)
from playhouse.postgres_ext import (
    JSONField,
    BinaryJSONField
)
from .base import BaseModel


class User(BaseModel):
    """用户模型.

    Attributes:
        uid (str): - uuid4定义的主键id,为了便于扩展不使用默认的自增主键
        nickname (str): - 用户的的昵称
        password (str): - 用户的的密码hash值,
        email (str): - 注册和发送的邮箱
        ctime (datetime): - 注册的时间
        info (json): - 其他信息

    """

    uid = UUIDField(primary_key=True)
    nickname = CharField(unique=True)
    password = CharField()
    email = CharField()
    ctime = DateTimeField()
    info = BinaryJSONField()

    @classmethod
    def hash_password(cls,org_pwd: str):
        """原始密码计算hash值.

        使用hmac计算hash值,salt被设置在`datebase`对象的`salt`字段上.

        Args:
            org_pwd (str): - 原始密码

        Returns:
            (str): 原始密码计算hash值的16进制表示.

        """
        salt = cls.Meta.database.salt.encode("utf-8")
        org_pwd = org_pwd.encode("utf-8")
        hash_pwd = hmac.new(salt, org_pwd)
        return hash_pwd.hexdigest()

    @classmethod
    async def current_user(cls, session):
        """获取当前session指定的user实例.

        Args:
            org_pwd (str): - 原始密码

        Returns:
            (str): 原始密码计算hash值的16进制表示

        """
        uid = session['uid']
        user = await cls.get(cls.uid == uid)
        return user

    def check_password(self, org_pwd):
        """判断用户密码是否正确.

        Args:
            org_pwd (str): - 输入的密码

        Returns:
            [bool]: - 是否输入的密码的hash值和保存的密码hash值一致

        """
        hash_pwd = User.hash_password(org_pwd)
        if self.password == hash_pwd:
            return True
        else:
            return False
