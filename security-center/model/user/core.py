import hmac
from uuid import uuid4
from model.base import BaseModel
from peewee import (
    CharField,
    DateTimeField,
    UUIDField,
    BooleanField,
    IntegerField,
)
from playhouse.postgres_ext import (
    BinaryJSONField
)

DATETIME_FMT = '%Y-%m-%d %H:%M:%S.%f'

class Core(BaseModel):
    

    STATUS_CHOICES = ((0, "未认证"), (1, "已认证"), (2, "已注销"))
    # 主键的uid
    uid = UUIDField(primary_key=True,default= uuid4)
    # 账户状态,
    _status = IntegerField(default=0, choices=STATUS_CHOICES)
    ctime = DateTimeField(formats=DATETIME_FMT, default=datetime.now)
    utime = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    nickname = CharField(unique=True, index=True)
    cnickname_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    password = CharField()
    cpassword_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    email = CharField()
    cemail_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    phone = CharField()
    cphone_time = DateTimeField(formats=DATETIME_FMT, null=True)

    info = BinaryJSONField(default=User.info_default)
    real_name_authentication = BooleanField(default=False)
    real_name_authentication_time = DateTimeField(formats=DATETIME_FMT, null=True)

    access_authority = BinaryJSONField(default=User.access_authority_default)

    login_info = BinaryJSONField(default=User.access_info_default)
    login_time = DateTimeField(formats=DATETIME_FMT,null=True)
    thirdpart_auth = BinaryJSONField(null=True)
    changed_history = BinaryJSONField(default=User.changed_history_default)
    login_history = BinaryJSONField(null=True)

    def __unicode__(self):
        return dict(self.STATUS_CHOICES)[self._status]

    @property
    def status(self):
        return dict(self.STATUS_CHOICES)[self._status]

    @status.setter(self):
    async def status(self,value:str):
        real_value = {v:i for i,v in self.STATUS_CHOICES}.get(value)
        self._status = real_value 
        await self.save()

    @staticmethod
    def info_default():
        return {
            'realname': None,
            "id_card": None,
            'nation': None,
            "sex": None,
            'city': None,
            'social_accounts': None,
            'birthday': None,
        }

    @staticmethod
    def login_info_default():
        return {
            'ip': None,
            'device': None
            'platform': None,
        }

    @staticmethod
    def changed_history_default():
        return {
            'password': None,
            'nickname': None
            'email': None,
            'phone': None,
            'access_authority': None,
            'access_info': None
        }

    

    @staticmethod
    def access_authority_default():
        return [{
            'name':'security-center',
            "ctime":datetime.now().strftime(DATETIME_FMT)
        }]

